#! /usr/bin/python
# -*- coding: utf-8 -*-

# Vibe Definer
# Nicholas DiBari
# Python script to generate mood of song from lyrics

from keys import MUSIXMATCH_KEY, TEXT_ANALYTICS_KEY
from models import Song

import requests
import webbrowser

# Base API URLs 
MUSIX_BASE = 'http://api.musixmatch.com/ws/1.1/'
TEXT_ANALYTICS_BASE = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0'

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
                     .format(MUSIX_BASE, MUSIXMATCH_KEY, code)

        lyrics_response = requests.get(lyrics_url)
        lyrics_resp_json = lyrics_response.json()['message']

        if lyrics_resp_json['header']['status_code'] == 200:
            print('Got lyrics of song {0} OK'.format(code))

        lyrics = lyrics_resp_json['body']['lyrics']['lyrics_body']

        # Get info from songs
        info_url = '{0}track.get?apikey={1}&track_id={2}'\
                   .format(MUSIX_BASE, MUSIXMATCH_KEY, code)

        info_response = requests.get(info_url)
        info_resp_json = info_response.json()['message']

        if info_resp_json['header']['status_code'] == 200:
            print('Got song info of song {0} OK'.format(code))

        artist = info_resp_json['body']['track']['artist_name']
        track_name = info_resp_json['body']['track']['track_name']

        # Package song
        song = Song(artist, track_name, lyrics)
        songs[code] = song
        print('Got lyrics and info for {0}: {1}'
              .format(song.name, song.artist))

    return songs

# Get Emotion
# Returns emotion of songs entered


def GetPositiveSongs(songs):
    i = 1
    pos_Songs = []

    for song in songs.itervalues():
        print('Gonna search sentiment for {0}'.format(song.name))

        # Prepare requests to Text Analytics API
        url = '{0}/sentiment'.format(TEXT_ANALYTICS_BASE)
        headers = {'Ocp-Apim-Subscription-Key': TEXT_ANALYTICS_KEY}
        json = {'documents': [
                                {"language": "en",
                                 "id": str(i),
                                 "text": song.lyrics
                                 }
                            ]
                }

        # Hit Text Analytics API
        sentiment_response = requests.post(url, headers=headers, json=json)
        sentiment_resp_json = sentiment_response.json()['documents']
        sentiment = sentiment_resp_json[0]['score']

        if sentiment > .5:
            print('Adding {0}: {1} as a positive track, sentiment: {2}'
                  .format(song.artist, song.name, sentiment))
            pos_Songs.append(song)
        
        i += 1
    return pos_Songs


def main():
    songs = GetLyrics()
    pos_Songs = GetPositiveSongs(songs)

    good_Song = pos_Songs[0]
    print('Gonna open {0} by {1}'.format(good_Song.name, good_Song.artist))
    
    song_URL = 'https://www.youtube.com/results?search_query={0} {1}'\
               .format(good_Song.artist, good_Song.name)

    webbrowser.open_new_tab(song_URL)


if __name__ == '__main__':
    main()
