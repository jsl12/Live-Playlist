import playlist as pl


class ArtistPlaylist(pl.Playlist):
    '''
    Playlist based on a list of artists
    '''

    def __init__(self):
        super().__init__()
        if self.logged_in:
            self.info("GPMAA login successful")
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
    ap = ArtistPlaylist()
    ap.search("King Gizzard")
    print("IDs of songs found")
    print([song['storeId'] for song in ap.results["King Gizzard"]])
    ap.api.logout()
