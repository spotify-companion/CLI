import spotify_client as spotify
import reddit_client as reddit
import os
from fuzzywuzzy import fuzz
from datetime import datetime
import billboard_client as billboard
import youtube_client as youtube


class AddSongs:
    __shared_instance = "AddSongs"

    @staticmethod
    def getInstance():
        '''Static access for singleton implementation '''
        if AddSongs.__shared_instance == "AddSongs":
            AddSongs()
        return AddSongs.__shared_instance

    def __init__(self):
        '''Virtual private constructor '''
        if AddSongs.__shared_instance != "AddSongs":
            raise Exception("Singleton pattern only allowed")
        else:
            AddSongs.__shared_instance = self
        self.spotify_client = spotify.SpotifyLogin().get_instance()
        self.spotify_client.refresh()
        self.sp = self.spotify_client.login()
        self.bill = billboard.Billboard()
        self.username = self.spotify_client.username
        self.user = self.sp.current_user()
        self.now = datetime.now().strftime('%d %b, %y')
        self.reddit_client = reddit.RedditClient().get_instance()
        self.youtube_client = youtube.YoutubeClient().get_instance()


    #TODO Add all the function implementations properly.
    def add_playlist_from_youtube(self):
        print("------Youtube to Spotify--------")
        print("Enter the playlist url")
        playlist_url = str(input())
        songs, playlist_name = self.youtube_client.get_playlist_songs(playlist_url)
        print(songs)
        self.make_playlist_with_songs(songs, playlist_name + " - Youtube Music Import", True)


    def add_playlist_from_reddit(self):
        print("Adding from the r/Listentothis subreddit:")  
        songs = self.reddit_client.get_songs()
        self.make_playlist_with_songs(songs, 'r/Listentothis Import on ' + self.now)
        

    def add_playlist_from_shazam(self):
        pass

    def add_playlist_from_offline(self,path_to_dir, name):
        curdir = os.chdir(path_to_dir)
        f = []
        for(dirpath, dirnames, filenames) in os.walk(os.curdir):
            f.extend(filenames)
            break
        names = []
        for i in f:
            if '.mp3' in i:
                names.append(i.split('.mp3')[0])
        # print(names)
        self.make_playlist(name)
        track_ids = self.get_track_ids(names)
        self.add_to_playlist(track_ids, name)

    def add_playlist_from_billboard(self):
        playlist_names = ['decade_end_hot_100',
        'year_end_hot_100',
        'hot_100']
        print("------Billboard playlist generator----------")
        print("This client enables you to generate a playlist based on billboard top charts. Select one of the following")
        print("1. Decade end hot 100\n2. Year end hot 100\n3. Hot 100")
        n = int(input())
        try:
            playlist_name = playlist_names[n-1]
        except:
            print("Not a valid choice, quitting...")
            return
        self.bill.CreatePlaylist(playlist_name)
        
        
        
    # Utility functions to make a playlist (Get track ids, get if playlist exists and so on):		
    def make_playlist(self,name):
        playlist_id = self.get_playlist_id(name)
        if playlist_id == '':
            self.sp.user_playlist_create(self.username,name)
        else:
            print("Playlist exists")


    def get_playlist_id(self,playlistname):
        playlistid = ''
        playlists = self.sp.user_playlists(self.username)
        for playlist in playlists['items']:
            if playlist['name'] == playlistname:
                playlistid = playlist['id']

        return playlistid


    def get_track_ids(self,data):
        track_ids = []
        for i in range(len(data)):
            try:
                results = self.sp.search(q=f"{data[i]}")
                if results['tracks']['total'] == 0:
                    continue
                else:
                    for j in range(len(results['tracks']['items'])):
                        # print(results['tracks']['items'][j])
                        track_ids.append(results['tracks']['items'][j]['id'])
                        # print(track_ids)
                        break
            except:
                continue
        print(track_ids)
        return track_ids

    def get_artists(self):
        final_results = []
        artists = []
        playlists = self.sp.user_playlists(self.username)
        for playlist in playlists['items']:
            # print(playlist['id'])
            res = self.user_playlist_tracks_full(self.username, playlist['id'])
            final_results.extend(res)
        for song in final_results:
            try:
                artists.extend(song['track']['artists'])
            except:
                continue

        return artists

    def user_playlist_tracks_full(self,playlist_id=None, fields=None, market=None):
        response = self.sp.user_playlist_tracks(
                self.user, playlist_id, fields=fields, limit=100, market=market)
        results = response["items"]
        while len(results) < response["total"]:
            response = self.sp.user_playlist_tracks(
                self.user, playlist_id, fields=fields, limit=100, offset=len(results), market=market)
            results.extend(response["items"])
        return results


    def add_to_playlist(self,tracks, playlistname):
        playlistID = self.get_playlist_id(playlistname)
        songs_in_playlist = self.user_playlist_tracks_full(
            playlist_id = playlistID)
        playlisttracks = []
        res = []
        for j in range(len(songs_in_playlist)):
            playlisttracks.append(songs_in_playlist[j]['track']['id'])
        for i in tracks:
            if i not in playlisttracks:
                    res.append(i)
        # print(res)

        self.sp.user_playlist_add_tracks(self.username, playlistID, res) if len(
            res) > 0 else print("All songs already in playlist")


    def make_playlist_with_songs(self,song_list, name, is_ytmusic = False):
        self.make_playlist(name)
        if is_ytmusic:
            songs = []
            for i in song_list:
                songs.append(i['title'])
            track_ids = self.get_track_ids(songs)
        else:
            track_ids = self.get_trackids_by_artist(song_list, [])
        self.add_to_playlist(track_ids, name)


    def get_trackids_by_artist(self,sample_data, titles=[],):
        track_ids = []
        for i in range(len(sample_data)):
            results = self.sp.search(
                q=f"{sample_data[i]['title']} {sample_data[i]['artist']} ", limit=5, type='track')
            # if track isn't on spotify as queried, go to next track
            print(results['tracks'])
            if results['tracks']['total'] == 0:
                continue
            else:
                for j in range(len(results['tracks']['items'])):
                    if fuzz.partial_ratio(results['tracks']['items'][j]['artists'][0]['name'], sample_data[i]['artist']) > 80 and fuzz.partial_ratio(results['tracks']['items'][j]['name'], sample_data[i]['title']) > 80:
                        track_ids.append(results['tracks']['items'][j]['id'])
                        break
                    else:
                        continue
        annotation_track_ids = []
        for title in titles:
            results = self.sp.search(q=f"{title} ", type='track')
            if results['tracks']['total'] == 0:
                continue
            else:
                annotation_track_ids.append(
                    results['tracks']['items'][0]['id'])
        track_ids = track_ids + annotation_track_ids
        # print("Got TrackIDs")
        return track_ids


if __name__ == '__main__':
    client = AddSongs().getInstance()
    client.add_playlist_from_billboard()