from artistplaylist import ArtistPlaylist
import object_writer
from contextlib import contextmanager

SAVE_FILE = 'genres.saved'

class SavingArtistPlaylist(ArtistPlaylist):
    def __init__(self, filename):
        super().__init__()
        self.writer = object_writer.ObjectWriter(filename)
        self.genres = self.writer.data if self.writer.data else set()

    def search(self, artist):
        res = super().search(artist)
        # Perform set union using the | operator
        self.genres |= set([r['genre'] for r in res])
        return res

    def save(self):
        self.writer.write(self.genres)

@contextmanager
def create_saving_playlist():
    playlist = SavingArtistPlaylist(SAVE_FILE)
    try:
        yield playlist
    finally:
        playlist.save()
        logging.info("Saved search results to {}".format(SAVE_FILE))


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    with create_saving_playlist() as ap:
        ap.search("Tupac")
        #print("IDs of songs found")
        #print([song['storeId'] for song in ap.results["King Gizzard"]])
        ap.api.logout()
