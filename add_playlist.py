import spotify_login

def add_playlist():
	spotifyClient = spotify_login.SpotifyLogin()
	spotifyClient.refresh()
	sp = spotifyClient.login()
	lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
	print(spotifyClient.username)
	results = sp.artist_top_tracks(lz_uri)
	for track in results['tracks'][:10]:
		print('track    : ' + track['name'])
		print('audio    : ' + track['preview_url'])
		print('cover art: ' + track['album']['images'][0]['url'])
		print()
		

	
if __name__ == '__main__':
	add_playlist()