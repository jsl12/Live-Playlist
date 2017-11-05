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

<<<<<<< HEAD
    def songs_from_artist(self, artist):
        res = self.api.search(artist)['song_hits']
        self.results[artist] = [x['track'] for x in res if artist in x['track']['artist']]
        return self.results[artist]
=======
    def search(self, artist):
        '''
        This is just a wrapper for Playlist.search that stores the results in a dictionary
        with the artist searched for as the key
        '''
        res = super().search(artist)
        self.results[artist] = res
        return res

>>>>>>> 23bdd137001c8073f80685a227070da11be08ab7

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    ap = ArtistPlaylist()
<<<<<<< HEAD
    artist = "Lonelyland"
    ap.songs_from_artist("Lonelyland")
    print([song['storeId'] for song in ap.results[artist]])
    ap.api.logout()
=======
    ap.search("King Gizzard")
    print("IDs of songs found")
    print([song['storeId'] for song in ap.results["King Gizzard"]])
    ap.api.logout()
>>>>>>> 23bdd137001c8073f80685a227070da11be08ab7
