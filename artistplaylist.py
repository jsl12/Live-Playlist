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
        res = self.api.search(artist)['song_hits']
        res = [song['track'] for song in res]
        return res

    def songs_from_artist(self, artist):
        res = self.search(artist)
        self.results[artist] = [song for song in res if artist in song['artist']]
        return self.results[artist]


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    ap = ArtistPlaylist()
    ap.songs_from_artist("King Gizzard")
    print("IDs of songs found")
    print([song['storeId'] for song in ap.results["King Gizzard"]])
    ap.api.logout()
