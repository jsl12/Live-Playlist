from setlist import *
from gmusicapi import Mobileclient, utils
import logging
from apikey import *

mlog = logging.getLogger(__name__)

utils.utils.per_client_logging = False
mlog.debug("gmusicapi logging monkey patch: {}".format(utils.utils.per_client_logging))


class gpmaa_playlist:
    'Class to handle logging into the GPMAA server and creating the playlist'

    def __init__(self, url, make=False):
        self.setup_logging()
        self.setlist = Setlist(url)
        self.api = Mobileclient()
        self.logged_in = self.api.login(EMAIL,
            TOKEN,
            Mobileclient.FROM_MAC_ADDRESS)
        if self.logged_in:
            self.search_for_songs()
            if make:
                self.make_playlist()

    def setup_logging(self):
        logger_name = '.'.join([__name__, __class__.__name__])
        self.logger = logging.getLogger(logger_name)
        logging.getLogger('gmusicapi.protocol.shared').setLevel(logging.INFO)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def make_playlist(self):
        self.songIDs = [self.resdict[s][0]['storeId'] for s in self.resdict.keys()]
        self.info("Creating playlist...")
        name = "{} - {}".format(self.setlist.artist, self.setlist.date)
        self.debug(name)
        desc = "{} live at {} on {}".format(self.setlist.artist,
            self.setlist.venue,
            self.setlist.date)
        self.debug(desc)
        self.id = self.api.create_playlist(name, desc)
        self.info("Playlist id: {}".format(self.id))
        self.debug("Song IDs {!s}".format(self.songIDs))
        self.api.add_songs_to_playlist(self.id, self.songIDs)
        return self.id

    def search_for_songs(self):
        self.info("Finding song info...")
        self.resdict = {name: [] for name in self.setlist.song_names}

        for song_name, r in self.resdict.items():
            query = "{} {}".format(self.setlist.artist, song_name)
            self.debug("Searching".ljust(20, '.') + query)
            results = self.api.search(query)['song_hits']
            results = [x['track'] for x in results]
            r.extend(results)
            self.debug("%d results found" % len(results))

    def print_results(self):
        for k, r in self.resdict.items():
            self.info("{:50}|{:35}|{:25}".format("Title", "Album", "Artist"))
            for result in r:
                t = result['title']
                alb = result['album']
                art = result['artist']
                self.info("{:50}|{:35}|{:25}".format(t, alb, art))
                self.info("-" * 110)

    def delete_playlist(self):
        self.info("Deleting playlist id: %s" % self.id)
        self.api.delete_playlist(self.id)
