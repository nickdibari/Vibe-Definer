#! /usr/bin/python
# -*- coding: utf-8 -*-

# Vibe Definer
# Nicholas DiBari
# Python script to generate mood of song from lyrics

from keys import MUSIXMATCH_KEY

import requests
from pprint import pprint

# Base API URL for Musixmatch API
MUSIX_BASE = 'http://api.musixmatch.com/ws/1.1/'

# GetLyrics
# Returns list of lyrics for analysis
def GetLyrics():
	song_IDs = []

	# Get list of songs 
	chart_url = '{0}chart.tracks.get?apikey={1}&page=1&page_size=10&f_has_lyrics=1'.format(MUSIX_BASE, MUSIXMATCH_KEY) 
	
	chart_response = requests.get(chart_url)
	chart_resp_json = chart_response.json()['message']

	if chart_resp_json['header']['status_code'] == 200:
		print('Got JSON of charts OK')

	track_list = chart_resp_json['body']['track_list']
	
	for i in range(len(track_list)):
		print('{0} has code of:'.format(track_list[i]['track']['track_name']))
		print(track_list[i]['track']['track_id'])
		song_IDs.append(track_list[i]['track']['track_id'])

def main():
	GetLyrics()

if __name__ == '__main__':
	main()