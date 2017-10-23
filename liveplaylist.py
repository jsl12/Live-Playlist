from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
from gmusicapi import Mobileclient, utils
import logging

utils.utils.per_client_logging = False
print("Logging ", utils.utils.per_client_logging)


class gpmaa_playlist:
	'Class to handle logging into the GPMAA server and creating the playlist'

	def __init__(self, url, make=False):
		self.setlist = setlist(url)
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


class setlist:

	def __init__(self, url):
		self.createBS(url)
		self.get_artist()
		self.get_song_names()
		self.get_venue()
		self.get_date()

	def createBS(self, url):
		print("Getting website...")
		r = requests.get(url).text

		print("Creating BeautifulSoup...")
		self.soup = BeautifulSoup(r, "html5lib")

	def get_song_names(self):
		print("Finding songs...")
		# song_tags = soup.find_all('a', attrs={"class": 'songLabel'})
		song_tags = self.soup.find_all('a', attrs={"class": re.compile('song')})

		self.song_names = []
		for tag in song_tags:
			self.song_names.append(tag.string)

	def get_artist(self):
		print("Finding artist...")
		artist_tag = self.soup.find('h1').find('a').find('span')
		if artist_tag:
			self.artist = artist_tag.string

	def get_venue(self):
		print("Finding venue...")
		venue_tag = self.soup.find('h1').find(text=re.compile('at')).next_sibling
		if venue_tag:
			self.venue = venue_tag.string

	def get_date(self):
		print("Finding date...")
		date_tag = self.soup.find(attrs={'class': re.compile('date')})
		month = str(date_tag.find(attrs={'class': re.compile('month')}).string)
		day = str(date_tag.find(attrs={'class': re.compile('day')}).string)
		year = str(date_tag.find(attrs={'class': re.compile('year')}).string)

		# month = datetime.strptime(month, '%b').tm_mon
		month = datetime.strptime(month, '%b').month

		date_string = "%s/%s/%s" % (month, day, year)

		self.date = datetime.strptime(date_string, "%m/%d/%Y").date()
		self.date = self.date.strftime("%m/%d/%y")

		# self.date = date(year=int(year))

	def __str__(self):
		s = self.artist + '\n'
		s += self.venue + '\n'
		s += self.date + '\n'
		s += str(self.song_names)
		return s