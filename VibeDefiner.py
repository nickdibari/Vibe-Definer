#! /usr/bin/python
# -*- coding: utf-8 -*-

# Vibe Definer
# Nicholas DiBari
# Python script to generate mood of song from lyrics

from keys import MUSIXMATCH_KEY, TEXT_ANALYTICS_KEY
from models import Song

import requests
import webbrowser
import json

# Base API URLs 
MUSIX_BASE = 'http://api.musixmatch.com/ws/1.1'
TEXT_ANALYTICS_BASE = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0'

# GetLyrics
# Returns list of lyrics for analysis from given artist


def GetLyrics(artist):
    songs = []

    # Get tracks from artist
    tracks_URL = '{0}/track.search?apikey={1}&q_artist={2}&page_size=10&f_has_lyrics=1'\
                 .format(MUSIX_BASE, MUSIXMATCH_KEY, artist)

    tracks_response = requests.get(tracks_URL)
    tracks_response.raise_for_status()
    
    tracks_json = tracks_response.json()['message']

    if tracks_json['header']['status_code'] == 200:
        print('Got tracks OK')

    tracks = tracks_json['body']['track_list']
    
    for i in range(len(tracks)):
        name = tracks[i]['track']['track_name']
        code = tracks[i]['track']['track_id']

        # Get Lyrics for song
        lyrics_url = '{0}/track.lyrics.get?apikey={1}&track_id={2}'\
                     .format(MUSIX_BASE, MUSIXMATCH_KEY, code)

        lyrics_response = requests.get(lyrics_url)
        lyrics_resp_json = lyrics_response.json()['message']

        if lyrics_resp_json['header']['status_code'] == 200:
            print('Got lyrics of song {0} OK'.format(name))

        lyrics = lyrics_resp_json['body']['lyrics']['lyrics_body']

        if not lyrics:
            lyrics = 'bad' # HACK HACK HACK HACK

        # Package song for analysis
        song = Song(code, artist, name, lyrics)
        songs.append(song)
        
        
    return songs


# Get Emotion
# Returns emotion of songs entered


def GetPositiveSongs(songs):
    i = 1
    pos_Songs = []

    print('Length of songs: {0}'.format(len(songs)))
    for song in songs:
        print('Gonna search sentiment for {0}'.format(song.name))
        lyrics = song.lyrics

        # Prepare requests to Text Analytics API
        url = '{0}/sentiment'.format(TEXT_ANALYTICS_BASE)
        headers = {'Ocp-Apim-Subscription-Key': TEXT_ANALYTICS_KEY}
        j = {'documents':[{"language": "en", "id": str(i), "text": song.lyrics}]}
        
        # Hit Text Analytics API
        sentiment_response = requests.post(url, data=None, headers=headers, json=j, params=None)
        sentiment_response.raise_for_status()
        
        sentiment_json = sentiment_response.json()['documents']
        sentiment = sentiment_json[0]['score']

        if sentiment > .5:
            print('Adding {0}: {1} as a positive track, sentiment: {2}'
                  .format(song.artist, song.name, sentiment))
            pos_Songs.append(song)
        
        i += 1
    return pos_Songs
    

def main():
    artist = raw_input('Please enter an artist to search for: ')
    songs = GetLyrics(artist)
    
    pos_Songs = GetPositiveSongs(songs)
    
    good_Song = pos_Songs[0]
    print('Gonna open {0} by {1}'.format(good_Song.name, good_Song.artist))

    song_URL = 'https://www.youtube.com/results?search_query={0} {1}'\
               .format(good_Song.artist, good_Song.name)

    webbrowser.open_new_tab(song_URL)


if __name__ == '__main__':
    main()
