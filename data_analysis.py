from click import style
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
import matplotlib.pyplot as plt
import seaborn as sns
import printing_essentials
from alive_progress import alive_bar


class AnalysePlaylist:


    def __init__(self):
        self.client = spotify.SpotifyLogin().get_instance()
        self.client.refresh()
        self.sp = self.client.login()
        self.username = self.client.username
        self.client_id = self.client.CLIENT_ID
        self.client_secret = self.client.CLIENT_SECRET
        self.name = self.sp.current_user()['display_name']
        sns.set_theme(style='darkgrid')
        self.console = printing_essentials.Printer().get_instance().console
        self.printer = printing_essentials.Printer().get_instance()



    def analyse_playlists(self, playlist_id):
        df = pd.DataFrame(columns = ['Name', 'Album', 'Artist', 'Year', 'Popularity', 'Duration','Tempo','Key', 'Valence', 'Liveness','Danceability', 'Instrumentalness', 'Acousticness', 'Energy'])
        self.data = df
        track_ids = []
        playlist = self.sp.playlist(playlist_id)
        name = self.sp.playlist(playlist_id)['name']
        # self.console.print(name)
        
        tracks = playlist['tracks']['items']
        offset = playlist['tracks']
        try:
            while offset['next']:
                offset = self.sp.next(offset)
                tracks.extend(offset['items'])
        except:
            self.console.print()
        length = len(tracks)
        self.console.print("There are " + str(len(tracks)) + " Tracks in " + name)
        for i in tracks:
            track_ids.append(i['track']['id'])

        with alive_bar(2, title = 'Fetching all songs',manual=True) as bar:
            count = 0   
            for i in track_ids:
                count+=1
                percentage = (count/length)
                bar(percentage)
                try:
                    if i is not None:
                        meta = self.sp.track(i)
                        features = self.sp.audio_features(i)
                        features = features[0];
                        # self.console.print(features)                    
                        track_dict = {

                                'Name' : meta['name'], 
                                'Album' : meta['album']['name'], 
                                'Artist' : meta['album']['artists'][0]['name'],
                                'Year' : meta['album']['release_date'][0:4], 
                                'Popularity' : meta['popularity'],
                                'Duration' : meta['duration_ms'] * 0.001  ,
                                'Danceability' : features['danceability'],
                                'Energy' : features['energy'],
                                'Key' : features['key'],
                                'Instrumentalness' : features['instrumentalness'],
                                'Valence' : features['valence'],
                                'Tempo' : features['tempo'],
                                'Liveness' : features['liveness'],
                                'Acousticness' : features['acousticness'],

                        }  
                        # self.console.print(track_dict) if count == 0 else self.console.print()          
                        df = df.append(track_dict, ignore_index = True, sort = False)
                        
                except: continue
            bar(1.0)
        # self.console.print(df)
        self.get_graphs(df, name)
        
    
    def get_graphs(self, df, name= "Default"):
        df = df.sort_values('Popularity', ascending = False)
        feature_list = ['Year', 'Popularity','Tempo','Key', 'Valence', 'Liveness','Danceability', 'Instrumentalness', 'Acousticness', 'Energy']
        numeric_data = df[feature_list]
        numeric_data = numeric_data.apply(pd.to_numeric)
        for i in feature_list:
            headers = ['Data', 'Value']
            title = "Analysis by " + i + " for " + name
            data = []
            data = []
            data.append(["Mean " + i, str(numeric_data[i].mean())[:5]])
            data.append(["Variance in " + i, str(numeric_data[i].var())]) 
            self.printer.printPlayList(data, headers, title)
            title = "Top songs by " + i
            top_df = df.sort_values(i, ascending = False)
            headers = ['Song', i]
            data = []
            # self.save_data(top_df, name, 'Top songs by' + i)
            for index, row in top_df.iterrows():
                data.append([row['Name'], str(row[i])])

            self.printer.printPlayList(data,headers,title)
        by_year = numeric_data.groupby('Year').mean().sort_values('Year').reset_index()
        # self.save_data(by_year, name,'Averages by Year')

        plt.figure(figsize=(12,8))
        sns.heatmap(numeric_data, annot = True)
        self.save_data(df,name)
        path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path + '/User Data Analysis')
        plt.savefig(name + '/' + 'Heatmap' + '.jpg')
        plt.savefig(name + '/' + 'Heatmap' + '.svg')
        sns.pairplot(data = numeric_data)
        plt.savefig(name + '/' + 'PairPlot' + '.jpg')
        plt.savefig(name + '/' + 'PairPlot' + '.svg')

        
    

    def analyse_user(self):
        playlists = self.sp.user_playlists(self.username)
        playlist_indices = {}
        index = 1
        playlist_header = ['Sl. No', 'Playlist Name']
        playlist_data_print = []
        for playlist in playlists['items']:
            playlist_data_print.append([str(index),playlist['name']])
            playlist_indices[index] = playlist
            index+=1
        self.printer.printPlayList(playlist_data_print, playlist_header, self.name)
        self.console.print("Select a playlist to be analysed:")
        n = int(input())
        while True:
            if n < 0 or n > index:
                self.console.print("Invalid input, please enter a correct number")
            else:
                break
        to_analyse = playlist_indices[n]
        self.console.print(to_analyse)
        self.analyse_playlists(to_analyse['uri'].split(':')[2])

    def save_data(self,df, name = "Default", sub_folder = ""):
        if name == 'r/listentothis': 
            name = 'listentothis'
        path = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists('User Data Analysis'):
            os.mkdir('User Data Analysis')
        os.chdir(path + '/User Data Analysis')
        if not os.path.exists(name):
            os.mkdir(name)
        if sub_folder == "":
            df.to_csv(name + '/' + self.name + ".csv")
        else:
            if not os.path.exists(os.curdir + '/' + sub_folder):
                os.mkdir(os.curdir + '/' + sub_folder)
                print(os.curdir)
            df.to_csv(name + '/' + sub_folder + '/' + self.name + '.csv')
        os.chdir(path)



if __name__ == '__main__':
    console = printing_essentials.Printer().get_instance().console
    console.rule("This is the data analysis section", style="green")
    console.print("Do you want to do an analysis of a public playlist or your own? Select 1 for public playlist, and 2 to list your playlists")
    n = int(input())
    if(n == 1):
        console.print("Paste a playlist uri to get data analysis done, preferably one with more than 50 songs:")
        uri = str(input())
        analyse = AnalysePlaylist()
        # analyse.jlt()
        analyse.analyse_playlists(playlist_id = uri[34:])
    elif(n == 2):
        console.print("Getting All your playlists.....")
        analyse = AnalysePlaylist()
        analyse.analyse_user()
