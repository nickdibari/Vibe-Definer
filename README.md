# Vibe-Definer
Python program to generate a positive sentiment song, according to the Microsoft Cloud Services API

## Requirements
In order to run this program, you will need to generate API Keys from the following sites:

Microsoft Cognitive Services Text Analytics: https://www.microsoft.com/cognitive-services/en-us/text-analytics-api

MusixMatch Lyrics: https://developer.musixmatch.com/documentation

Spotify: https://developer.spotify.com/

After you have generated keys for the three sites, save the keys in a file in the directory VibeDefiner is located in with the name keys.py. The file should look something like:
```python
# keys.py
MUSIXMATCH_KEY = 'your MusixMatch API key'
TEXT_ANALYTICS_KEY = 'your Microsoft API key'
SPOTIFY_ID = 'your Spotify API ID'
SPOTIFY_KEY = = 'your Spotify API key'
```

Pay careful attention to not push this file to any repositories! A useful tip is to create a text file named .gitignore and include keys.py in the file. This will ensure Git will not track the file and accidently add it to a commit.


## Usage
`python VibeDefiner.py`

Will prompt user for an artist to search for. Generates a list of positive sentiment songs and opens a youtube search query page for a random song from the list

## Installation
`git clone https://github.com/nickdibari/Vibe-Definer.git `

`cd Vibe-Definer`

`pip install -r requirements.txt`
