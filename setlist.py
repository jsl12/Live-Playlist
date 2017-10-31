from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

class Setlist:

	def __init__(self, url):
		# print("Creating Setlist...")
		self.create_BS(url)
		self.get_artist()
		self.get_song_names()
		self.get_venue()
		self.get_date()

	def create_BS(self, url):
		# print("Getting website...")
		r = requests.get(url).text

		# print("Creating BeautifulSoup...")
		self.soup = BeautifulSoup(r, "html5lib")

	def get_song_names(self):
		# print("Finding songs...")
		# song_tags = soup.find_all('a', attrs={"class": 'songLabel'})
		song_tags = self.soup.find_all('a', attrs={"class": re.compile('song')})

		self.song_names = []
		for tag in song_tags:
			self.song_names.append(tag.string)

	def get_artist(self):
		# print("Finding artist...")
		artist_tag = self.soup.find('h1').find('a').find('span')
		if artist_tag:
			self.artist = artist_tag.string

	def get_venue(self):
		# print("Finding venue...")
		venue_tag = self.soup.find('h1').find(text=re.compile('at')).next_sibling
		if venue_tag:
			self.venue = venue_tag.string

	def get_date(self):
		# print("Finding date...")
		date_tag = self.soup.find(attrs={'class': re.compile('date')})
		month = date_tag.find(attrs={'class': re.compile('month')}).string
		day = date_tag.find(attrs={'class': re.compile('day')}).string
		year = date_tag.find(attrs={'class': re.compile('year')}).string

		month = datetime.strptime(month, '%b').month

		date_string = "%s/%s/%s" % (month, day, year)

		self.date = datetime.strptime(date_string, "%m/%d/%Y").date()
		self.date = self.date.strftime("%m/%d/%y")

	def __str__(self):
		return "{0}\n{1}\n{2}\n{3}".format(
			self.artist,
			self.venue,
			self.date,
			str(self.song_names))
	