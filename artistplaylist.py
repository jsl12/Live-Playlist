import playlist as pl

class ArtistPlaylist(pl.Playlist):
    '''
    Playlist based on a list of artists
    '''

    def __init__(self, artists):
        super().__init__()

        if self.logged_in:
            print("GPMAA login successful")
            song_ids = []
            for a in artists:
                song_ids.append(self.song_from_artist(a))
            self.create_playlist(
                song_ids,
                name = "ArtistPlaylist",
                description = ""
                )

    def song_from_artist(self, artist):
        self.results = self.api.search(artist)['song_hits']
        self.results = [x['track'] for x in self.results]
        return self.results[0]['storeId']

if __name__ == '__main__':
    ap = ArtistPlaylist(["King Gizzard"])