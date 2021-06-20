
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotify_constants



class SpotifyLogin:
    __shared_instance = "SpotifyLogin"

    @staticmethod
    def get_instance():
        """ Static access for singleton implementation""" 

        if SpotifyLogin.__shared_instance == "SpotifyLogin":
            SpotifyLogin()
        
        return SpotifyLogin.__shared_instance

    def __init__(self):
        
        SpotifyLogin.__shared_instance = self
        self.scopes = 'playlist-modify-public playlist-modify-private user-read-private user-read-recently-played'
        self.CLIENT_ID = spotify_constants.login_constants['CLIENT_ID']
        self.CLIENT_SECRET = spotify_constants.login_constants['CLIENT_SECRET']
        self.REDIRECT_URI = spotify_constants.login_constants['REDIRECT_URI']
        self.spotifyOAuth = spotipy.SpotifyOAuth(client_id=self.CLIENT_ID,
                                    client_secret=self.CLIENT_SECRET,
                                    redirect_uri=self.REDIRECT_URI,
                                    scope=self.scopes)

        self.token = self.spotifyOAuth.get_access_token()
        self.spotifyObject = spotipy.Spotify(auth=self.token['access_token'])
        self.setUsername()

    def login(self):
        return self.spotifyObject;

    def refresh(self):
        if self.spotifyOAuth.is_token_expired(self.token) == True:
            print("Refreshing token, it has expired...")
            self.token = self.spotifyOAuth.get_access_token()
            self.spotifyObject = spotipy.Spotify(auth = self.token['access_token'])

    def setUsername(self):
        user = self.spotifyObject.current_user()
        self.username = user['id']


