# Spotify-Companion



A CLI application for getting various metrics from the spotify API, as well as making playlists and analysing data.




# Table of contents

- [Usage](#usage)
- [Installation](#installation)
- [Features](#features)
- [Uninstallation](#uninstallation)
- [License](#license)

# Usage

1. To ensure that spotify-companion works, you need to have python and pip installed.
2. If configured correctly, running
``` bash
$ python3 main.py 
```
(OR in WINDOWS)
```bash
> python main.py 
```
Should start the CLI script.



# Installation

[(Back to top)](#table-of-contents)

### To install requirements, run

```bash
pip install requirements.txt
```
Replace pip with pip3 if running on linux or macos.






# Features

[(Back to top)](#table-of-contents)

1. Song recommendations:
	- Spotify API based recommendations by tracks, or artists that can be converted into a new playlist from the command line.
	- Custom generated recommendations that uses a form of K-Means Clustering to generate songs recommended by *Playlist*
	- Generate recommendations on a model trained over 600k songs to classify into clusters.

2. Playlist addition from other platforms:
	- Add songs and make a new spotify playlist from:
		- Youtube Music Public Playlists
		- Shazam Tracks that are fetched by an automated script
		- Billboard playlists
		- Offline folders with tracks
		- A particular subreddit with songs (r/listentothis)
	
3. Analyse data from a playlist:
	- Analyse data either from:
		- Personal playlists 
		- Public spotify playlists
	
	- Data such as top songs by popularity, year and various other parameters including acousticness, danceability, valence, liveness and so on are generated.
	- Data is saved as svg or jpg files and as csv files for Pandas DataFrames
	- Data is also displayed on the CLI with pretty printing and table forms.





# License

[(Back to top)](#table-of-contents)


The MIT License (MIT) 2017 - [Spotify Companion](https://github.com/orgs/spotify-companion/dashboard). Please have a look at the [LICENSE.md](LICENSE.md) for more details.