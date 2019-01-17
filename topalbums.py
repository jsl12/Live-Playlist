from apikey import *
from bs4 import BeautifulSoup
import requests
import re
import gmusicapi
import logging
import jellyfish

mlog = logging.getLogger(__name__)
gmusicapi.utils.utils.per_client_logging = False

url = 'https://www.kexp.org/countdowns/kexp-listeners-top-903-albums-2018/'
soup = BeautifulSoup(requests.get(url).text, 'html5lib')

regex = re.compile('\xa0(.*)')
artists = [regex.search(tag.parent.text).group(1).strip() for tag in soup.find_all('big')]

regex = re.compile('(.*)\(.*\)')
albums = [regex.search(tag.text.strip()).group(1).strip() for tag in soup.find_all('h4')]

gm = gmusicapi.Mobileclient()
gm.login(EMAIL, TOKEN, gmusicapi.Mobileclient.FROM_MAC_ADDRESS)

# playlist_id = gm.create_playlist(
#     'KEXP Top Listener Albums 2018',
#     r'Created by scraping https://www.kexp.org/countdowns/kexp-listeners-top-903-albums-2018/'
# )
playlist_id = gm.get_all_playlists()[-1]['id']
for i, a in enumerate(artists):
    try:
        artist_id = gm.search(a)['artist_hits'][0]['artist']['artistId']
    except:
        print('No artist id found for: {}'.format(a))
        continue

    try:
        album_id = [a for a in gm.get_artist_info(artist_id)['albums'] if jellyfish.jaro_distance(albums[i], a['name'].upper()) > .7][0]['albumId']
    except:
        print('No album id found for {}'.format(albums[i]))
        continue

    try:
        song_ids = [s['storeId'] for s in gm.get_album_info(album_id)['tracks']]
    except:
        print('No song ids for {}'.format(album_id))
        continue

    gm.add_songs_to_playlist(playlist_id, song_ids)
    continue