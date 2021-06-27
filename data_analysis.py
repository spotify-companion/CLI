import requests
import pandas as pd
import spotipy
import spotipy.util as util
from sklearn.cluster import KMeans
from sklearn import preprocessing
import matplotlib.pyplot as plt
import spotify_client as spotify
import os
from datetime import datetime

class AnalysePlaylist:


    def __init__(self):
        self.client = spotify.SpotifyLogin().get_instance()
        self.client.refresh()
        self.sp = self.client.login()
        self.username = self.client.username
        self.client_id = self.client.CLIENT_ID
        self.client_secret = self.client.CLIENT_SECRET
        self.name = self.sp.current_user()['display_name']
        print(self.name)



    def analyse_playlists(self, playlist_id):
        df = pd.DataFrame(columns = ['Name', 'Album', 'Artist', 'Year', 'Popularity', 'Duration'])
        
        track_ids = []
        playlist = self.sp.playlist(playlist_id)
        name = self.sp.playlist(playlist_id)['name']
        print(name)
        
        tracks = playlist['tracks']['items']
        offset = playlist['tracks']
        try:
            while offset['next']:
                offset = self.sp.next(offset)
                tracks.extend(offset['items'])
        except:
            print()
            
        print(len(tracks))
        for i in tracks:
            track_ids.append(i['track']['id'])
            
        for i in track_ids:
            # print(i)
            try:
                if i is not None:
                    meta = self.sp.track(i)          
                    
                    track_dict = {

                            'Name' : meta['name'], 
                            'Album' : meta['album']['name'], 
                            'Artist' : meta['album']['artists'][0]['name'],
                            'Year' : meta['album']['release_date'][0:4], 
                            'Popularity' : meta['popularity'],
                            'Duration' : meta['duration_ms'] * 0.001  ,

                    }            
                    df = df.append(track_dict, ignore_index = True, sort = False)
            except: continue

        print(df)
        self.save_data(df, name)
        
        dataset = df.filter(['Year', 'Popularity'])
        print(dataset)
    
    def analyse_user(self):
        playlists = self.sp.user_playlists(self.username)
        playlist_indices = {}
        index = 1
        for playlist in playlists['items']:
            print(str(index) + " : " + playlist['name'])
            playlist_indices[index] = playlist
            index+=1
        print("Select a playlist to be analysed:")
        n = int(input())
        while True:
            if n < 0 or n > index:
                print("Invalid input, please enter a correct number")
            else:
                break
        to_analyse = playlist_indices[n]
        print(to_analyse)
        self.analyse_playlists(to_analyse['uri'].split(':')[2])

    def save_data(self,df, name = "Default"):
        path = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists('User Data Analysis'):
            os.mkdir('User Data Analysis')
        os.chdir(path + '/User Data Analysis')
        if not os.path.exists(name):
            os.mkdir(name)
        df.to_csv(name + '/' + self.name + ".csv")
        os.chdir(path)



if __name__ == '__main__':

    
    print("--------This is the data analysis section.---------")
    print("Do you want to do an analysis of a public playlist or your own? Select 1 for public playlist, and 2 to list your playlists")
    n = int(input())
    if(n == 1):
        print("Paste a playlist uri to get data analysis done, preferably one with more than 50 songs:")
        uri = str(input())
        analyse = AnalysePlaylist()
        analyse.analyse_playlists(playlist_id = uri[34:])
    elif(n == 2):
        print("Getting All your playlists.....")
        analyse = AnalysePlaylist()
        analyse.analyse_user()
