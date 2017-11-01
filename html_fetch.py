from bs4 import BeautifulSoup
import logging
import requests

def create_soup(url):
	logging.info("Fetching {0}".format(url))
	r = requests.get(url).text
	#logging.info("Creating BeautifulSoup...")
	return BeautifulSoup(r, "html5lib")