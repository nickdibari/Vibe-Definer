#! /usr/bin/python
# -*- coding: utf-8 -*-

# Vibe Definer
# Nicholas DiBari
# Python script to generate mood of song from lyrics

from keys import MUSIXMATCH_KEY
from models import Song

import requests

# Base API URL for Musixmatch API
MUSIX_BASE = 'http://api.musixmatch.com/ws/1.1/'

# GetLyrics
# Returns list of lyrics for analysis


def GetLyrics():
    song_IDs = []
    songs = {}

    # Get list of songs
    chart_url = '{0}chart.tracks.get?apikey={1}&page=1&page_size=10&\
    f_has_lyrics=1'.format(MUSIX_BASE, MUSIXMATCH_KEY)

    chart_response = requests.get(chart_url)
    chart_resp_json = chart_response.json()['message']

    if chart_resp_json['header']['status_code'] == 200:
        print('Got JSON of charts OK')

    track_list = chart_resp_json['body']['track_list']

    for i in range(len(track_list)):
        song_IDs.append(track_list[i]['track']['track_id'])

    for code in song_IDs:
        # Get lyrics from songs
        lyrics_url = '{0}track.lyrics.get?apikey={1}&track_id={2}'\
        .format(MUSIX_BASE, MUSIXMATCH_KEY, song_IDs[2])
        
        lyrics_response = requests.get(lyrics_url)
        lyrics_resp_json = lyrics_response.json()['message']
        
        if lyrics_resp_json['header']['status_code'] == 200:
            print('Got lyrics of song {0} OK'.format(code))
        
        lyrics = lyrics_resp_json['body']['lyrics']['lyrics_body']

        # Get info from songs
        info_url = '{0}track.get?apikey={1}&track_id={2}'\
        .format(MUSIX_BASE, MUSIXMATCH_KEY, song_IDs[2])

        info_response = requests.get(info_url)
        info_resp_json = info_response.json()['message']

        if info_resp_json['header']['status_code'] == 200:
            print('Got song info of song {0} OK'.format(code))

        artist = info_resp_json['body']['track']['artist_name']
        track_name = info_resp_json['body']['track']['track_name']
        
        # Package song 
        song = Song(artist, track_name, lyrics)
        songs[code] = song

    return songs
    
    
def main():
    songs = GetLyrics()



if __name__ == '__main__':
    main()
