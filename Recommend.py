import random
import spotipy
import requests
import pandas as pd
from sklearn import metrics
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


class Recommend:

    '''

    Arguments - 
    client_id     - unique client ID
    client_secret - unique secret key 
    username      - unique Spotify username

    '''

    def __init__(self, client_id = None, client_secret = None, username = None):

        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username       
        self.url = 'https://api.spotify.com/v1/recommendations?'
        self.market = 'US'
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


    def print_response(self, query):

        token = self.generate_token()
        response = requests.get(query, headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
        json_response = response.json()

        try:
            print('Recommendations:\n')
            for i, j in enumerate(json_response['tracks']):
                print(f"{i+1}) \"{j['name']}\" : {j['artists'][0]['name']}")
            print()

        except:
            print(json_response)


    def byArtistSpotify(self, artist = None, number = None):

        if artist is None:
            print('Enter the artist as a string argument\n')
        if number is None:
            number = 10
        artist_result = self.sp.search(artist)

        try:
            seed_artists = artist_result['tracks']['items'][0]['artists'][0]['uri'][15:]
            seed_genres = []
            seed_genres_entire = self.sp.artist(seed_artists)

            if len(seed_genres_entire) < 3:
                seed_genres = seed_genres_entire
            else:
                for i in seed_genres_entire['genres'][:3]:
                    seed_genres.append(i)

            query = f'{self.url}limit={number}&market={self.market}&seed_genres={seed_genres}&seed_artists={seed_artists}'
            print(self.print_response(query))

        except:
            print('Seed artists for given artist could not be generated\n')


    def byTrackSpotify(self, track_URI = None, number = None):
        
        if track_URI is None:
            print('Enter the track_URI as a string argument\n')            
        if number is None:
            number = 10
        track_ID = track_URI.split(':')[2]

        try:
            meta = self.sp.track(track_ID)
            artist = meta['album']['artists'][0]['name']
            artist_result = self.sp.search(artist)

            try:
                seed_artists = artist_result['tracks']['items'][0]['artists'][0]['uri'][15:]
                seed_genres = []
                seed_genres_entire = self.sp.artist(seed_artists)

                if len(seed_genres_entire) < 3:
                    seed_genres = seed_genres_entire
                else:
                    for i in seed_genres_entire['genres'][:3]:
                        seed_genres.append(i)

                query = f'{self.url}limit={number}&market={self.market}&seed_genres={seed_genres}&seed_artists={seed_artists}&seed_tracks={track_ID}'
                print(self.print_response(query))

            except:
                print('Seed artist for given track could not be generated\n')

        except:
            print('Recheck track_URI argument\n')

            
    def byPlaylistSpotify(self, playlist_URL = None, number = None):
        
        if number is None:
            number = 10            
        if playlist_URL is None:
            print('Recheck playlist_URL argument\n')

        playlist_id = playlist_URL[34:]
        df = pd.DataFrame(columns = ['Name', 'Album', 'Artist', 'Year', 'Duration', 'Danceability', 'Energy'])        
        track_ids = []
        
        for i in self.sp.playlist(playlist_id)['tracks']['items']:
            track_ids.append(i['track']['id'])
            
        for i in track_ids:
            meta = self.sp.track(i)
            features = self.sp.audio_features(i)
            
            track_dict = {
                'Name' : meta['name'], 
                'Album' : meta['album']['name'], 
                'Artist' : meta['album']['artists'][0]['name'],
                'Year' : meta['album']['release_date'][0:4], 
                'Duration' : meta['duration_ms'] * 0.001,
                'Danceability' : features[0]['danceability'],
                'Energy' : features[0]['energy']
            } 
            
            df = df.append(track_dict, ignore_index = True, sort = False)
        
        common_artist = self.sp.search(df['Artist'].value_counts().head(1))
        seed_artists = common_artist['tracks']['items'][0]['artists'][0]['uri'][15:]
        seed_genres = []
        seed_genres_entire = self.sp.artist(seed_artists)

        if len(seed_genres_entire) < 3:
            seed_genres = seed_genres_entire
        else:
            for i in seed_genres_entire['genres'][:3]:
                seed_genres.append(i)

        seed_tracks = random.choice(track_ids)
        target_danceability = round(df['Danceability'].mean(), 1)
        target_energy = round(df['Energy'].mean(), 1)
        
        try:
            query = f'{self.url}limit={number}&market={self.market}&seed_genres={seed_genres}'
            query += f'&target_danceability={target_danceability}'
            query += f'&target_energy={target_energy}'
            query += f'&seed_artists={seed_artists}&seed_tracks={seed_tracks}'
            print(self.print_response(query))
            
        except:
            print('Query could not be executed\n')


    def byAudioFeaturesSpotify(self, target_acousticness = None, target_danceability = None, target_duration_ms = None, target_energy = None, target_instrumentalness = None, target_key = None, target_liveness = None, target_loudness = None, target_mode = None, target_popularity = None, target_speechiness = None, target_tempo = None, target_time_signature = None, target_valence = None, artist = None):

        if artist is None:
            print('Enter the artist as a string argument\n')
        artist_result = self.sp.search(artist)

        try:
            seed_artists = artist_result['tracks']['items'][0]['artists'][0]['uri'][15:]
            seed_genres = []
            seed_genres_entire = self.sp.artist(seed_artists)

            if len(seed_genres_entire) < 3:
                seed_genres = seed_genres_entire
            else:
                for i in seed_genres_entire['genres'][:3]:
                    seed_genres.append(i)

            query = f'{self.url}limit={10}&market={self.market}&seed_genres={seed_genres}'
            
            if target_acousticness is not None:
                query += f'&target_acousticness={target_acousticness}'
            if target_danceability is not None:
                query += f'&target_danceability={target_danceability}'
            if target_duration_ms is not None:
                query += f'target_duration_ms={target_duration_ms}'
            if target_energy is not None:
                query += f'target_energy={target_energy}'
            if target_instrumentalness is not None:
                query += f'target_instrumentalness={target_instrumentalness}'
            if target_key is not None:
                query += f'target_key={target_key}'
            if target_liveness is not None:
                query += f'target_liveness={target_liveness}'
            if target_loudness is not None:
                query += f'target_loudness={target_loudness}'
            if target_mode is not None:
                query += f'target_mode={target_mode}'
            if target_popularity is not None:
                query += f'target_popularity={target_popularity}'
            if target_speechiness is not None:
                query += f'target_speechiness={target_speechiness}'
            if target_tempo is not None:
                query += f'target_tempo={target_tempo}'
            if target_time_signature is not None:
                query += f'target_time_signature={target_time_signature}'
            if target_valence is not None:
                query += f'target_valence={target_valence}'
            
            query += f'&seed_artists={seed_artists}'
            print(self.print_response(query))

        except:
            print('Seed artists for given artist could not be generated\n')


    def byTrack(self, track_URL = None, number = None, query = None, cluster = None):

        if track_URL is None:
            print('Recheck track_URL argument\n')
        track_ID = track_URL[31:].split('?')[0]
        if number is None:
            number = 10       
        if query is None and cluster is None:
            print('Specify method of recommendation as boolean argument\n')
        if query is True and cluster is True:
            print('Specify single method of recommendation as boolean argument\n')
        
        if query == True:
                    
            meta = self.sp.track(track_ID)
            features = self.sp.audio_features(track_ID)
            target_year = meta['album']['release_date'][0:4]        
            target_popularity = meta['popularity']
            target_danceability = features[0]['danceability']
            target_energy = features[0]['energy']

            tracks_df = pd.read_csv('tracks.csv')
        
            try:
                results = pd.DataFrame()
                results = tracks_df.loc[(tracks_df['popularity'] >= max(0, target_popularity - 2))
                            & (tracks_df['popularity'] < target_popularity + 1)
                            & (tracks_df['energy'] >= max(0, target_energy - 0.1))
                            & (tracks_df['energy'] < target_energy + 0.1)
                            & (tracks_df['danceability'] >= max(0, target_danceability - 0.1))
                            & (tracks_df['danceability'] < target_danceability + 0.1)
                            & (tracks_df['release_date'].str.startswith(str(target_year))),['name', 'popularity', 'artists', 'release_date']
                                       ]

                count = 1
                results = results.sort_values(by = ['popularity'], ascending = False).head(number)
                print('Recommendations :')    
                for result in range(len(results)):
                    print(count, ') ', results.iloc[result, 0], ' : ', results.iloc[result, 2], sep = '')
                    count += 1
            
            except:
                print('Recommendations could not be generated\n')

        if cluster == True:

            clusters_df = pd.read_csv('Clusters/Clusters.csv')
            cluster = int(clusters_df.loc[clusters_df['id'] == track_ID].iloc[0, 5])
            target_popularity = int(clusters_df.loc[clusters_df['id'] == track_ID].iloc[0, 4])
            results = pd.DataFrame()
            results = clusters_df.loc[
                  (clusters_df['cluster'] == cluster)
                & (clusters_df['popularity'] >= max(0, target_popularity - 2))
                & (clusters_df['popularity'] < target_popularity + 2)
                                     ]
            results = results.sort_values(by = ['popularity'], ascending = False).head(number)
            
            count = 1
            print('Recommendations :')    
            for result in range(len(results)):
                print(count, ') ', results.iloc[result, 2], ' : ', results.iloc[result, 3], sep = '')
                count += 1


    def byPlaylist(self, playlist_URL = None):

        if playlist_URL is None:
            print('Recheck playlist_URL argument\n')
                
        playlist_id = playlist_URL[34:]
        dataset = pd.DataFrame(columns = ['Year', 'Popularity', 'Energy', 'Danceability'])        
        track_ids = []
                
        for i in self.sp.playlist(playlist_id)['tracks']['items']:
            track_ids.append(i['track']['id'])
                    
        for i in track_ids:
            meta = self.sp.track(i)
            features = self.sp.audio_features(i)
                    
            track_dict = {
                'Year' : meta['album']['release_date'][0:4], 
                'Popularity' : meta['popularity'],
                'Energy' : features[0]['energy'],
                'Danceability' : features[0]['danceability']
            }            
            dataset = dataset.append(track_dict, ignore_index = True, sort = False)

        dataset_copy1 = pd.DataFrame()
        dataset_copy1 = dataset.filter(['Year', 'Popularity'])
        dataset_copy1['Year'] = pd.to_numeric(dataset_copy1['Year'])
        
        X = StandardScaler().fit_transform(dataset_copy1)
        prev_silhoutte = 0
        prev_CH = 0
        count = 1

        for i in range(2, 11):
            k_means = KMeans(n_clusters = i)
            silhoutte = metrics.silhouette_score(X, k_means.labels_, metric = 'euclidean')
            CH = metrics.calinski_harabasz_score(X, k_means.labels_)
                    
            if (silhoutte > prev_silhoutte and CH > prev_CH):
                prev_silhoutte = silhoutte
                prev_CH = CH
                pass
                    
            else:
                dataset_copy = pd.DataFrame()
                dataset_copy = dataset.filter(['Year', 'Popularity'])
                dataset_copy['Year'] = pd.to_numeric(dataset_copy['Year'])
                KMeans(i).fit(preprocessing.scale(dataset_copy))
                clusters_df = dataset.copy()
                clusters_df['Cluster'] = KMeans(i).fit_predict(preprocessing.scale(dataset))
                            
                for cluster in range(0, i):
                    temp = clusters_df.copy()
                    single_cluster_df = temp.loc[temp['Cluster'] == cluster]
                        
                    single_cluster_df['Year'] = pd.to_numeric(single_cluster_df['Year'])
                    single_cluster_df = single_cluster_df.reset_index()
                    single_cluster_df = single_cluster_df.filter(['Year', 'Popularity', 'Energy', 'Danceability', 'Cluster'])
                                
                    target_year = int(round(single_cluster_df['Year'].mean()))
                    target_year_2 = target_year - 1
                    target_year_3 = min(2020, target_year + 1)
                    target_popularity = int(round(single_cluster_df['Popularity'].mean()))
                    target_energy = round(single_cluster_df['Energy'].mean(), 2)
                    target_danceability = round(single_cluster_df['Danceability'].mean(), 2)
                    tracks_df = pd.read_csv('tracks.csv')

                    results1 = pd.DataFrame()
                    results1 = tracks_df.loc[(tracks_df['popularity'] >= max(0, target_popularity - 2))
                                & (tracks_df['popularity'] <= target_popularity + 2)
                                & (tracks_df['energy'] >= max(0, target_energy - 0.05))
                                & (tracks_df['energy'] <= target_energy + 0.05)
                                & (tracks_df['danceability'] >= max(0, target_danceability - 0.05))
                                & (tracks_df['danceability'] <= target_danceability + 0.05)          
                                & (tracks_df['release_date'].str.startswith(str(target_year))),['name', 'popularity', 'artists', 'release_date']
                                                ]
                    results2 = pd.DataFrame()
                    results2 = tracks_df.loc[(tracks_df['popularity'] >= max(0, target_popularity - 2))
                                & (tracks_df['popularity'] <= target_popularity + 2)
                                & (tracks_df['energy'] >= max(0, target_energy - 0.05))
                                & (tracks_df['energy'] <= target_energy + 0.05)
                                & (tracks_df['danceability'] >= max(0, target_danceability - 0.05))
                                & (tracks_df['danceability'] <= target_danceability + 0.05)          
                                & (tracks_df['release_date'].str.startswith(str(target_year_2))),['name', 'popularity', 'artists', 'release_date']
                                                ]
                    results3 = pd.DataFrame()
                    results3 = tracks_df.loc[(tracks_df['popularity'] >= max(0, target_popularity - 2))
                                & (tracks_df['popularity'] <= target_popularity + 2)
                                & (tracks_df['energy'] >= max(0, target_energy - 0.05))
                                & (tracks_df['energy'] <= target_energy + 0.05)
                                & (tracks_df['danceability'] >= max(0, target_danceability - 0.05))
                                & (tracks_df['danceability'] <= target_danceability + 0.05)          
                                & (tracks_df['release_date'].str.startswith(str(target_year_3))),['name', 'popularity', 'artists', 'release_date']
                                            ]
                            
                    results = pd.DataFrame()
                    results = pd.concat([results1, results2, results3])
                    results = results.drop_duplicates(subset = ['name', 'popularity', 'artists', 'release_date'], keep = False)
                    print('Recommendations for cluster :', cluster + 1)
                        
                    if results.empty:
                        print('No recommendations for cluster', cluster + 1)                           
                        
                    results = results.sort_values(by = ['popularity'], ascending = False).head(5)

                    for result in range(len(results)):
                        print(count, ') ', results.iloc[result, 0], ' : ', results.iloc[result, 2], sep = '')
                        count += 1                         
                    print()
                                                    
                break


    def byAudioFeatures(self, target_acousticness = None, target_danceability = None, target_duration_ms = None, target_energy = None, target_instrumentalness = None, target_key = None, target_liveness = None, target_loudness = None, target_mode = None, target_popularity = None, target_speechiness = None, target_tempo = None, target_time_signature = None, target_valence = None):
        
        tracks_df = pd.read_csv('tracks.csv')
        results = pd.DataFrame()

        if target_acousticness is not None:
            results = tracks_df.loc[(tracks_df['acousticness'] >= max(0,target_acousticness - 0.05)) & (tracks_df['acousticness'] <= target_acousticness + 0.05)]
        if target_danceability is not None:
            try:
                results = results.loc[(tracks_df['danceability'] >= max(0, target_danceability - 0.05)) & (tracks_df['danceability'] <= target_danceability + 0.05)]
            except:
                pass
        if target_duration_ms is not None:
            try:
                results = results.loc[(tracks_df['duration_ms'] >= max(0, target_duration_ms - 120000)) & (tracks_df['duration_ms'] <= target_duration_ms + 120000)]
            except:
                pass
        if target_energy is not None:
            try:
                results = results.loc[(tracks_df['energy'] >= max(0, target_energy - 0.05)) & (tracks_df['energy'] <= target_energy + 0.05)]
            except:
                pass
        if target_instrumentalness is not None:
            try:
                results = results.loc[(tracks_df['instrumentalness'] >= max(0, target_instrumentalness - 0.05)) & (tracks_df['instrumentalness'] <= target_instrumentalness + 0.05)]
            except:
                pass
        if target_key is not None:
            try:
                results = results.loc[(tracks_df['key'] >= max(0, target_key - 2)) & (tracks_df['key'] <= target_key + 0.05)]
            except:
                pass
        if target_liveness is not None:
            try:
                results = results.loc[(tracks_df['liveness'] >= max(0, target_liveness - 0.05)) & (tracks_df['liveness'] <= target_liveness + 0.05)]
            except:
                pass
        if target_loudness is not None:
            try:
                results = results.loc[(abs(tracks_df['loudness']) >= max(0, target_loudness - 2)) & (abs(tracks_df['loudness']) <= target_loudness + 2)]
            except:
                pass
        if target_mode is not None:
            try:
                results = results.loc[(tracks_df['mode'] == target_mode)]
            except:
                pass
        if target_popularity is not None:
            try:
                results = results.loc[tracks_df['popularity'] >= max(0, target_popularity - 2) & (tracks_df['popularity'] <= target_popularity + 2)]
            except:
                pass
        if target_speechiness is not None:
            try:
                results = results.loc[(tracks_df['speechiness'] >= max(0, target_speechiness - 0.05)) & (tracks_df['speechiness'] <= target_speechiness + 0.05)]
            except:
                pass
        if target_tempo is not None:
            try:
                results = results.loc[tracks_df['tempo'] >= max(0, target_tempo - 25) & (tracks_df['tempo'] <= target_tempo + 25)]
            except:
                pass
        if target_time_signature is not None:
            try:
                results = results.loc[(tracks_df['time_signature'] >= max(0, target_time_signature - 1)) & (tracks_df['time_signature'] <= target_time_signature + 1)]
            except:
                pass
        if target_valence is not None:
            try:
                results = results.loc[(tracks_df['valence'] >= max(0, target_valence - 0.05)) & (tracks_df['valence'] <= target_valence + 0.05)]
            except:
                pass

        if results.empty:
            print('No recommendations')                           
                                
        results = results.head(5)

        count = 1
        for result in range(len(results)):
            print(count, ') ', results.iloc[result, 1], ' : ', results.iloc[result, 5], sep = '')
            count += 1                         


if __name__ == '__main__':

    username = 'adityabhat'
    client_id = 'a527b948b8cc4aaba97a38ae3170b736'
    client_secret = '0adeba9418364a788b9d0d2458ffbd44'


    R = Recommend(client_id = client_id, client_secret = client_secret, username = username)
    #R.byArtistSpotify(artist = 'Oasis')
    #R.byTrackSpotify(track_URI = 'spotify:track:4wnVn683GT0XAGdR1PtC33')
    #R.byPlaylistSpotify(playlist_URL = 'https://open.spotify.com/playlist/6Oi7R7boGek1iv7WXH01Bm?si=0b4105221a9f41ad', number = 10)
    #R.byAudioFeaturesSpotify(target_duration_ms = 180000, artist = 'Drake')
 
    #R.byTrack(track_URL = 'https://open.spotify.com/track/5HNCy40Ni5BZJFw1TKzRsC?si=cd04a63b17dc4ed4', cluster=True)
    #R.byPlaylist(playlist_URL = 'https://open.spotify.com/playlist/37i9dQZF1E4uKxUut7eXtk?si=0cef77d575fd4bdb')
    R.byAudioFeatures(target_duration_ms = 300000)