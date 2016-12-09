# Class Definitions for VibeDefiner

# Song Object


class Song(object):
    """Object to hold Song artist/track name/lyrics"""
    def __init__(self, artist, track_name, lyrics):
        self.artist = artist
        self.name = track_name
        self.lyrics = lyrics
