import requests
import pandas as pd
import spotipy
import spotipy.util as util
from sklearn.cluster import KMeans
from sklearn import preprocessing
import matplotlib.pyplot as plt
import spotify_login
import os
from datetime import datetime

class AnalysePlaylist:

    '''

    Arguments - 
    client_id     - unique client ID provided
    client_secret - unique secret key provided for the client ID
    username      - unique Spotify username
    playlist_name - name of playlist in user's library

    '''

    def __init__(self,playlist_id = None):
        self.client = spotify_login.SpotifyLogin()
        self.client.refresh()
        self.sp = self.client.login()
        self.username = self.client.username
        self.client_id = self.client.CLIENT_ID
        self.client_secret = self.client.CLIENT_SECRET
        self.playlist_id = playlist_id
        self.name = self.sp.current_user()['display_name']
        print(self.name)

        self.sp = spotipy.Spotify(auth = self.generate_token())

    def generate_token(self):
        post_response = requests.post('https://accounts.spotify.com/api/token', {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })
        post_respose_json = post_response.json()
        token = post_respose_json['access_token']

        return token

    def AnalysePlaylist(self):
        df = pd.DataFrame(columns = ['Name', 'Album', 'Artist', 'Year', 'Popularity', 'Duration'])
        
        track_ids = []
        
        for i in self.sp.playlist(self.playlist_id)['tracks']['items']:
            track_ids.append(i['track']['id'])
            
        for i in track_ids:
            meta = self.sp.track(i)           
            
            track_dict = {

                'Name' : meta['name'], 
                'Album' : meta['album']['name'], 
                'Artist' : meta['album']['artists'][0]['name'],
                'Year' : meta['album']['release_date'][0:4], 
                'Popularity' : meta['popularity'],
                'Duration' : meta['duration_ms'] * 0.001             

            }            
            df = df.append(track_dict, ignore_index = True, sort = False)

        #print(df)

        dataset = pd.DataFrame()
        self.save_data(df)
        
        dataset = df.filter(['Year', 'Popularity'])
        print(dataset)
    
    def save_data(self,df):
        if not os.path.exists('User Data Analysis'):
            os.mkdir('User Data Analysis')
        df.to_csv('./User Data Analysis/' + self.name + datetime.now().strftime('%H:%m') + '.csv')



if __name__ == '__main__':

    
    print("--------This is the data analysis section.---------")
    print("Paste a playlist uri to get data analysis done, preferably one with more than 50 songs:")
    uri = str(input())
    playlist_URL = 'https://open.spotify.com/playlist/6Oi7R7boGek1iv7WXH01Bm?si=eea123a346fa4bb8'

    analyse = AnalysePlaylist(playlist_id = playlist_URL[34:])
    analyse.AnalysePlaylist()