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

    def songs_from_artist(self, artist):
        self.results[artist] = [x['track'] for x in self.api.search(artist)['song_hits']]
        return self.results[artist]

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    ap = ArtistPlaylist()
    ap.songs_from_artist("King Gizzard")
    print([song['storeId'] for song in ap.results["King Gizzard"]])
    ap.api.logout()