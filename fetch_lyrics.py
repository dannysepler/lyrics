import yaml
import requests
import os, json, sys

secrets = yaml.load(open('conf/secrets.yml', 'r'))
MUSIXMATCH = 'https://api.musixmatch.com/ws/1.1/'

def queryTopHundredTracks():
	
	GET_TRACKS = 'chart.tracks.get'
	parameters = {
		'apikey' : secrets['api']['apikey'],
		'f_has_lyrics': 1,
		'chart_name': 'top',
		'page_size': 100,
		'country': 'us',
		'page': 1
	}

	response = requests.get(
		MUSIXMATCH + GET_TRACKS, params=parameters
	)

	data = response.json()
	file = open('data/top_songs.json', 'w+')

	file.write(json.dumps(data, indent=4))

def getLyricsAndOutputToText(track_id, commontrack_id, path):

	GET_LYRICS = 'track.lyrics.get'
	parameters = {
		'apikey': secrets['api']['apikey'],
		'track_id': track_id,
		'commontrack_id': commontrack_id
	}

	response = requests.get(
		MUSIXMATCH + GET_LYRICS, params=parameters
	)

	data = response.json()
	lyrics_body = data['message']['body']['lyrics']['lyrics_body']
	lyrics_body = lyrics_body.replace(secrets['songs']['musixmatch_ending'], '')
	file = open(path, 'w+')
	file.write(lyrics_body)
	
def displayTopSongs():
	file = open('data/top_songs.json', 'r').read()
	song_data = json.loads(file)
	tracks = song_data['message']['body']['track_list']

	# Loop through tracks
	for track in tracks:

		# Get all important information
		artist_name = track['track']['artist_name']
		track_name = track['track']['track_name']
		track_id = track['track']['track_id']
		commontrack_id = track['track']['commontrack_id']
		
		# Create folder if it doesn't exist
		path = 'lyrics/%s' % artist_name
		if not os.path.exists(path):
			os.makedirs(path)

		# Create song file, insert lyrics
		filename = track_name + '.txt'
		path = os.path.join(path, filename)
		getLyricsAndOutputToText(track_id, commontrack_id, path)
		print('Created ' + path)

	print('Successfully created %i tracks' % len(tracks))



# RUN HERE
queryTopHundredTracks()
displayTopSongs()
