import reddit_client
import spotify_login

def listen_to_this():
        rclient = reddit_client.RedditClient()
	client = spotify_login.SpotifyLogin()
	client.refresh()
	sp = client.login()
	username = client.username
        songlist, titles = rclient.getHot('listentothis', 20)
        songs = []
        for i in titles:
            if ' -- ' in i:
                i = i.split(' -- ')
            elif ' - ' in i:
                i = i.split(' - ')
            elif ' — ' in i:
                i = i.split(' — ')
            # print(i[len(i)-1].split(' [')[0])
            temp = {'artist': i[0], 'title': i[len(i)-1].split(' [')[0]}
            songs.append(temp)

        sp.make_playlist_with_songs(songs, 'r/listentothis')
        return sp.user_playlist_tracks_full(username, sp.get_playlist_id('r/listentothis'))
