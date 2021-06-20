from ytmusicapi import YTMusic


class YoutubeClient:
    __shared_instance = "YoutubeClient"
    @staticmethod
    def get_instance():
        """ To implement singleton pattern """ 
        if YoutubeClient.__shared_instance == "YoutubeClient":
            YoutubeClient()
        
        return YoutubeClient.__shared_instance

    def __init__(self):
        if YoutubeClient.__shared_instance != "YoutubeClient":
            raise Exception("Sorry this is a singleton implementation")
        else:
            YoutubeClient.__shared_instance = self
        
        self.client = YTMusic()

    def get_playlist_songs(self, playlist_url):
        playlist_id = self.get_id(playlist_url)
        print(playlist_id)
        playlist_items = self.client.get_playlist(playlist_id)
        songs = []
        # print(playlist_items)
        playlist_name = playlist_items['title']
        
        for track in playlist_items['tracks']:
            temp = {}
            print(track)
            temp['title'] = track['title']
            try:
                temp['artist'] = track['artists'][0]
            except:
                temp['artist'] = track['artist']['name']
            songs.append(temp)
            
        return songs, playlist_name


    def get_id(self, playlist_url):
        try:
            return playlist_url.split("=")[1].split('&')[0]

        except ValueError:
            print("Invalid URL Value")


    
if __name__ == "__main__":
    pass