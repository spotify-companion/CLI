import requests
import pandas as pd
import spotipy
import spotipy.util as util
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import spotify_client as spotify

class Billboard:

    '''

    Arguments - 
    client_id     - unique client ID provided
    client_secret - unique secret key provided for the client ID
    username      - unique Spotify username
    playlist_name - type of billboard chart to convert

    '''

    def __init__(self,playlist_name = None):
        self.playlist_name = playlist_name
        self.client = spotify.SpotifyLogin().get_instance()
        self.client.refresh()
        self.sp = self.client.login()
        self.username = self.client.username
        self.token = self.client.token
        

        

    def CreatePlaylist(self,playlist_name):

        self.sp.user_playlist_create(self.username, name = playlist_name)
        if (playlist_name == 'decade_end_hot_100'):
            self.URL = 'https://www.billboard.com/charts/decade-end/hot-100'
        if (playlist_name == 'year_end_hot_100'):
            self.URL = 'https://www.billboard.com/charts/year-end/hot-100-songs'
        if (playlist_name == 'hot_100'):
            self.URL = 'https://www.billboard.com/charts/hot-100'

        
        playlists = self.sp.user_playlists(self.username)
        for playlist in playlists['items']:
            if playlist['name'] == self.playlist_name:
                playlist_id = playlist['id']
        
        
        soup = BeautifulSoup(requests.get(self.URL).content,'html.parser')
        songs = []
        artists_temp = []
        
        for song in soup('div', class_ = 'ye-chart-item__title'):
            temp = song.contents[0]
            songs.append(temp[1:len(song.contents[0]) - 1])

        for artist in soup('div', class_ = 'ye-chart-item__artist'):
            temp = artist.contents[0]

            if(temp[1:len(artist.contents[0]) - 1] == ''):
                temp2 = artist.find("a").contents[0]
                artists_temp.append(temp2[1:len(artist.find("a").contents[0]) - 1])

            artists_temp.append(temp[1:len(artist.contents[0]) - 1])

        artists = []
        for string in artists_temp:
            if (string != ''):
                artists.append(string)

        billboard_df = pd.DataFrame({'Title' : songs, 'Artist' : artists})

        track_ids = []
        for i in range(len(billboard_df)):
            results = self.sp.search(q=f"{billboard_df['Title'][i]}", limit = 5, type = 'track')
            if results['tracks']['total'] == 0:
                continue
            else:
                for j in range(len(results['tracks']['items'])):
                    if fuzz.partial_ratio(results['tracks']['items'][j]['artists'][0]['name'], billboard_df['Artist'][i]) > 90 and fuzz.partial_ratio(results['tracks']['items'][j]['name'], billboard_df['Title'][i]) > 90 :
                        track_ids.append(results['tracks']['items'][j]['id'])
                        break
                    else:
                        continue

        self.sp.user_playlist_add_tracks(self.username, playlist_id, track_ids)


if __name__ == '__main__':
    pass