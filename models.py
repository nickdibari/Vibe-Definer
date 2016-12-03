# Class Definitions for VibeDefiner

# Song Object
class Song(object):
	"""Object to hold Song lyrics/artist/name/genre"""
	def __init__(self, artist, track_name, genre, lyrics):
		self.artist = artist
		self.name = track_name
		self.genre = genre
		self.lyrics = lyrics
		
		