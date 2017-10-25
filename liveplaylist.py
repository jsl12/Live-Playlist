from setlist import *
from gmusicapi import Mobileclient, utils
import logging

utils.utils.per_client_logging = False
print("gmusicapi logging monkey patch:", utils.utils.per_client_logging)


class gpmaa_playlist:
	'Class to handle logging into the GPMAA server and creating the playlist'

	def __init__(self, url, make=False):
		self.setlist = Setlist(url)
		self.api = Mobileclient()
		self.logged_in = self.api.login('lancaster.js@gmail.com',
			'oitufqltzwpxdkau',
			Mobileclient.FROM_MAC_ADDRESS)
		if self.logged_in:
			# self.get_all_songIDs()
			self.search_for_songs()
			if make:
				self.make_playlist()

	def make_playlist(self):
		'Creates the playlist withing GPMAA'
		if self.songIDs:
			print("Creating playlist...")
			name = "%s - %s" % (self.setlist.artist,
				self.setlist.date)
			print(name)
			desc = "%s live at %s on %s" % (self.setlist.artist,
				self.setlist.venue,
				self.setlist.date)
			print(desc)
			self.id = self.api.create_playlist(name, desc)
			print("Playlist id: %s" % self.id)

			self.api.add_songs_to_playlist(self.id, self.songIDs)
		return self.id

	def search_for_songs(self):
		print("Finding song info...")
		self.resdict = {name: [] for name in self.setlist.song_names}

		for song_name, r in self.resdict.items():
			query = ("%s %s" % (self.setlist.artist, song_name))
			logging.info(query.center(50, '-'))
			results = self.api.search(query)['song_hits']
			results = [x['track'] for x in results]
			# results = [(x['title'],
			# 			x['artist'],
			# 			x['album'],
			# 			x['storeId'])
			# 			for x in results]
			# logging.info(results)
			r.extend(results)
			logging.info("%d results found" % len(results))

	def print_results(self):
		for k, r in self.resdict.items():
			print("{:50}|{:35}|{:25}".format("Title", "Album", "Artist"))
			for result in r:
				t = result['title']
				alb = result['album']
				art = result['artist']
				print("{:50}|{:35}|{:25}".format(t, alb, art))
				print("-" * 110)

	def get_all_songIDs(self):
		self.songIDs = []
		for name in self.setlist.song_names:
			self.songID(name)

	def songID(self, songName):
		logging.info(songName.center(50, '-'))
		try:
			id = None
			artist = self.setlist.artist
			query = "%s %s" % (artist, songName)
			songs = self.api.search(query)['song_hits']
			self.songIDs.append(self.select_song(songs, songName))
		except IndexError as e:
			print("Song not found")
		except UnicodeEncodeError:
			pass

		return id

	def select_song(self, results, songName):
		if hasattr(self, "results"):
			self.results.append(results)
		else:
			self.results = [results]

		s = ' ' * 5
		s += "%d songs" % len(results)
		logging.info(s)

		if results:
			found = results[0]
			track = found['track']
			id = track['storeId']
			album = track['album']

			# creates a tuple (title, album, storeId) based on which tracks have matching names
			# used to filter incorrect songs when they appear on an album with the same name as the query
			song_versions = [(r['track']['title'], r['track']['album'],
				r['track']['storeId']) for r in results
				if re.search(songName, r['track']['title'])]

			# filters the song_versions list by which songs have 'Live' in the title
			live_versions = [song for song in song_versions if re.search('Live',
				song[0])]
			if live_versions:
				id = live_versions[0][2]
				print("%d Live versions found" % len(live_versions))

			s = '\n'
			for i in range(len(song_versions)):
				s += str(song_versions[i]) + '\n'
			logging.info(s)
			return id

	def clean(self):
		print("Deleting playlist id: %s" % self.id)
		self.api.delete_playlist(self.id)
