import random
import requests
import pandas as pd
import spotify_login


class SpotifyRecommend:

    '''

    Arguments - None
    spotifyclient = client from login method

    '''

    def __init__(self):
        self.client = spotify_login.SpotifyLogin()
        self.client.refresh()
        self.sp = self.client.login()
        self.url = 'https://api.spotify.com/v1/recommendations?'
        self.market = 'US'
        self.username = self.client.username

    def generate_token(self):
        post_response = requests.post('https://accounts.spotify.com/api/token', {
            'grant_type': 'client_credentials',
            'client_id': self.client.CLIENT_ID,
            'client_secret': self.client.CLIENT_SECRET,
        })
        post_respose_json = post_response.json()
        token = post_respose_json['access_token']

        return token

    def print_response(self, query):
        token = self.generate_token()

        response = requests.get(query, headers={
                                "Content-Type": "application/json", "Authorization": f"Bearer {token}"})
        json_response = response.json()

        try:
            print('Recommended Songs : ')
            for i, j in enumerate(json_response['tracks']):
                print(f"{i+1}) \"{j['name']}\" : {j['artists'][0]['name']}")
            print()
            return json_response['tracks']
        except:
            print(json_response)

            return json_response

    def artist_top_songs(self, artist=None, number=10):
        # artist - string argument containing name of artist

        if artist is None:
            print('Enter artist name as an argument to get their top songs')
            print()

        artist_result = self.sp.search(artist)
        artistURI = artist_result['tracks']['items'][0]['artists'][0]['uri']
        tracks = self.sp.artist_top_tracks(artistURI)

        print('Recommended Songs:')
        for track in tracks['tracks'][:number]:
            print('"' + track['name'] + '"' ' :', artist)
        print()

    def artist_similar_songs(self, artist=None, number=10):
        # artist - string argument containing name of artist

        if artist is None:
            print('Enter artist name as an argument for similar recommendations')
            print()

        artist_result = self.sp.search(artist)
        try:
                seed_artists = artist_result['tracks']['items'][0]['artists'][0]['uri'][15:]
                seed_genres = []
                genre_result = self.sp.artist(seed_artists)
                for genre in genre_result['genres'][:3]:
                    seed_genres.append(genre)

                query = f'{self.url}limit={number}&market={self.market}&seed_genres={seed_genres}'
                query += f'&seed_artists={seed_artists}'

                print(self.print_response(query))
        except:
                print("No seed artists for the artist generated by spotify! We are sorry for the same!")

    def track_similar_songs(self, trackURI=None, number=10):
        # trackURI - list containing track URI's as strings

        seed_tracks = trackURI

        for i in range(len(seed_tracks)):
            try:
                i = i.split(':')[2]
            except:
                continue

        results = self.sp.recommendations(seed_tracks=seed_tracks)

        print('Recommended Songs : ')
        for track in results['tracks'][:number]:
            print('"' + track['name'] + '"' ' :', track['artists'][0]['name'])
        print()

    def playlist_similar_songs(self, playlistURI=None, number=10):
        # playlistURI - string argument containing only playlist URI

        def get_track_features(ID):

            meta = self.sp.track(ID)
            features = self.sp.audio_features(ID)

            track = [

                meta['name'],
                meta['album']['artists'][0]['name'],
                features[0]['danceability'],
                features[0]['energy'],

            ]

            return track

        def track_to_dataframe(URI):

            trackIDs = []
            playlist = self.sp.user_playlist(self.username, URI)

            for song in playlist['tracks']['items']:
                trackIDs.append(song['track']['id'])

            tracks = []

            for i in range(len(trackIDs)):
                track = get_track_features(trackIDs[i])
                tracks.append(track)

            data = pd.DataFrame(
                tracks, columns=['Song', 'Artist', 'Danceability', 'Energy'])

            return data

        try:
            playlistURI = playlistURI.split(':')[2]
        except:
            playlistURI = playlistURI

        df = track_to_dataframe(playlistURI)

        artist_result = self.sp.search(df['Artist'].value_counts().head(1))
        seed_artists = artist_result['tracks']['items'][0]['artists'][0]['uri'][15:]

        trackIDs = []
        playlist = self.sp.user_playlist(self.username, playlistURI)
        for song in playlist['tracks']['items']:
            trackIDs.append(song['track']['id'])

        seed_tracks = random.choice(trackIDs)

        seed_genres = []
        genre_result = self.sp.artist(seed_artists)
        for genre in genre_result['genres'][:3]:
            seed_genres.append(genre)

        target_danceability = round(df['Danceability'].mean(), 1)
        target_energy = round(df['Energy'].mean(), 1)

        query = f'{self.url}limit={number}&market={self.market}&seed_genres={seed_genres}'
        query += f'&target_danceability={target_danceability}'
        query += f'&target_energy={target_energy}'
        query += f'&seed_artists={seed_artists}'
        query += f'&seed_tracks={seed_tracks}'

        res = self.print_response(query)
        return res;


def recommend_main():
    recommender = SpotifyRecommend()
    print("---------- This is the spotify recommendation system-------------")
    print("Select an option :\n" +
          "1. Recommend by artist\n2. Recommend by track\n3. Recommend by playlist")
    choice = int(input())
    if choice == 1:
            print('You have chosen to get recommendation by artist\nEnter the artist name')
            artist = str(input())
            recommender.artist_similar_songs(artist)

    elif choice == 2:
            print('You have chosen to get recommendation by track\nEnter the track url')
            track = str(input())
            recommender.artist_similar_songs(track)	

    elif choice == 3:
           print("You have chosen to get recommended by playlist.\nEnter the playlist URI")
           playlist = str(input())
           recommender.playlist_similar_songs(playlist)
    else:
           print("Not a valid option. Quitting...")





    

if __name__ == '__main__':
    recommend_main()
