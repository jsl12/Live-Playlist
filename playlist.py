from setlist import *
from gmusicapi import Mobileclient, utils
import logging
from apikey import *

mlog = logging.getLogger(__name__)

utils.utils.per_client_logging = False
mlog.debug("gmusicapi logging monkey patch: {}".format(utils.utils.per_client_logging))


class Playlist():
    '''
    Parent class for specific types of playlists, like:
        Live Setlist Playlist
            setlist based on the set of songs played at a live concert
        Upcoming Concert Playlist
            setlist generated from a list of bands that have upcoming concerts in an area
    '''

    def __init__(self, make=False):
        self.setup_logging()
        self.api = Mobileclient()
        self.logged_in = self.api.login(EMAIL,
            TOKEN,
            # Mobileclient.FROM_MAC_ADDRESS)
            DEVICE_ID)

    def setup_logging(self):
        logger_name = '.'.join([__name__, __class__.__name__])
        self.logger = logging.getLogger(logger_name)
        logging.getLogger('gmusicapi.protocol.shared').setLevel(logging.INFO)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)

    def error(self, msg):
        self.logger.error(msg)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def search(self, query):
        '''
        This function got pulled to the parent class because we'll always be searching
        for things and wanting the song results. They're always going to have to be
        processed this way because of how the search result is formatted.

        The result is a list of song dictionaries with keys such as storeId, artist, etc.
        '''
        res = self.api.search(artist)['song_hits']
        res = [song['track'] for song in res]
        return res

    def create_playlist(self, song_ids, name, description='', public=False):
        self.info("Creating {}".format(name))
        self.id = self.api.create_playlist(name, description, public)
        self.api.add_songs_to_playlist(self.id, song_ids)

    def delete_playlist(self):
        if hasattr(self, 'id') and self.id is not None:
            self.info("Deleting playlist id: %s".format(self.id))
            self.api.delete_playlist(self.id)
        else:
            self.info("Can't delete a playlist without its id")