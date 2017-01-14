#! /usr/bin/python
# -*- coding: utf-8 -*-

# Vibe Definer
# Nicholas DiBari
# Python script to generate mood of song from lyrics

from keys import MUSIXMATCH_KEY, TEXT_ANALYTICS_KEY, SPOTIFY_ID, SPOTIFY_KEY
from models import Song

import spotipy
from spotipy import oauth2

import requests
import webbrowser
import random

# Base API URLs
MUSIX_BASE = 'http://api.musixmatch.com/ws/1.1'

TEXT_ANALYTICS_BASE = 'https://westus.api.cognitive.microsoft.com/\
text/analytics/v2.0'

# GetLyrics
# Returns list of lyrics for analysis from given artist


def GetLyrics(artist):
    songs = []

    # Get tracks from artist
    tracks_URL = '{0}/track.search?apikey={1}&q_artist={2}&page_size=20&f_has_lyrics=1'\
                 .format(MUSIX_BASE, MUSIXMATCH_KEY, artist)

    tracks_response = requests.get(tracks_URL)
    tracks_response.raise_for_status()

    tracks_json = tracks_response.json()['message']

    if tracks_json['header']['status_code'] == 200:
        print('Got JSON of track.search OK')

    tracks = tracks_json['body']['track_list']

    for track in tracks:
        name = track['track']['track_name'].encode('ascii', 'ignore')
        code = track['track']['track_id']

        # Get Lyrics for song
        lyrics_url = '{0}/track.lyrics.get?apikey={1}&track_id={2}'\
                     .format(MUSIX_BASE, MUSIXMATCH_KEY, code)

        lyrics_response = requests.get(lyrics_url)
        lyrics_json = lyrics_response.json()['message']

        if lyrics_json['header']['status_code'] == 200:
            print('Got JSON of track.lyrics.get from {0}'.format(name))

        else:
            print('Something went wrong for song {0}'.format(name))

        if lyrics_json['body']:
            lyrics = lyrics_json['body']['lyrics']['lyrics_body']

            if not lyrics:
                print('No lyrics found for {0}'.format(name))
                lyrics = 'bad' # Can't pass None Type to Text Analytics API

            else:
                print('Found lyrics for {0} OK'.format(name))

        else:
            print('No body for song {0}'.format(name))

        # Package song for analysis
        song = Song(artist, name, lyrics)
        songs.append(song)

    return songs


# Get Emotion
# Returns emotion of songs entered


def GetPositiveSongs(songs):
    i = 0
    pos_Songs = []
    url = '{0}/sentiment'.format(TEXT_ANALYTICS_BASE)
    headers = {'Ocp-Apim-Subscription-Key': TEXT_ANALYTICS_KEY}
    j = {'documents': []}

    # Package song names/lyrics into JSON Body
    for song in songs:
        j['documents'].append({'language': 'en', 'id': song.name, 'text': song.lyrics})

    # Send JSON Body through API
    sentiment_response = requests.post(url, data=None, headers=headers, json=j, params=None)    
    sentiment_response.raise_for_status()

    sentiment_json = sentiment_response.json()['documents']

    # Decode API Response and determine if song should be saved
    for resp in sentiment_json:
        if resp['score'] > .5:
            print('Appending {0} to positive songs'.format(resp['id']))
            pos_Songs.append(songs[i])

        i += 1

    return pos_Songs


# SongAnalysis
# Analyze music of positive songs and return positive music songs


def SongAnalysis(songs):
    results = []

    # Authentication for Spotify API
    creds = oauth2.SpotifyClientCredentials(client_id=SPOTIFY_ID, client_secret=SPOTIFY_KEY)

    conx = spotipy.Spotify(client_credentials_manager=creds)

    if conx:
        print('Connected to Spotify API OK')

    for song in songs:
        song_id = None

        print('Gonna search valence for: {0}'.format(song.name))

        # Search for track ID for given song name
        search_results = conx.search(q=song.name, type='track')

        if search_results:
            print('Got JSON of search OK')

        else:
            print('DID NOT get JSON of search')

        search_JSON = search_results['tracks']['items']

        for resp in search_JSON:
            if resp['artists'][0]['name'] == song.artist:
                print('Found match for song {0} with artist {1}'.format(song.name, song.artist))
                song_id = resp['id']
                break

        if song_id == None:
            print('Did not find match for song {0} by {1}'.format(song.name, song.artist))

        else:
            song_IDs = [song_id]

            # Search for audio features of given track
            features_results = conx.audio_features(tracks=song_IDs)

            if features_results:
                print('Got JSON of audio_features OK')

            else:
                print('DID NOT get JSON of audio_features')

            features_JSON = features_results[0]

            valence = features_JSON['valence']

            if valence > .5:
                print('Adding {0} to results, valence: {1}'.format(song.name, valence))
                results.append(song)

    return results


def main():
    artist = raw_input('Please enter an artist to search for: ')
    songs = GetLyrics(artist)

    pos_Songs = GetPositiveSongs(songs)
    print('Got {0} songs backs from GetPositiveSongs'.format(len(pos_Songs)))

    good_Songs = SongAnalysis(pos_Songs)
    print('Got {0} songs backs from SongAnalysis'.format(len(good_Songs)))

    good_Song = random.choice(good_Songs)

    print('Gonna open {0} by {1}'.format(good_Song.name, good_Song.artist))

    song_URL = 'https://www.youtube.com/results?search_query={0} {1}'\
               .format(good_Song.artist, good_Song.name)

    webbrowser.open_new_tab(song_URL)

if __name__ == '__main__':
    main()
