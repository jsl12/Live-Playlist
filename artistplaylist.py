import playlist as pl


class ArtistPlaylist(pl.Playlist):
    '''
    Playlist based on a list of artists
    '''

    def __init__(self):
        super().__init__()
        if self.logged_in:
            self.results = {}

    def search(self, artist):
        '''
        This is just a wrapper for Playlist.search that stores the results in a dictionary
        with the artist searched for as the key
        '''
        res = super().search(artist)
        self.results[artist] = res
        return res


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    ARTIST = "King Gizzard"

    ap = ArtistPlaylist()
    print("Searching for {}".format(ARTIST))
    ap.search(ARTIST)
    print("Songs found:")
    for song in ap.results[ARTIST]:
        print("{} | {:40} | {}".format(song['storeId'], song['album'], song['title']))
    ap.api.logout()
