import liveplaylist as lp
import logging

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)

test_url = ("https://www.setlist.fm/setlist/king-gizzard-and-the-lizard-wizard/2018/stubbs-bar-b-q-austin-tx-33ea30e5.html")

setlist = lp.Setlist(test_url)
print(setlist)

p = lp.LivePlaylist(test_url)
p.make_playlist()
p.api.logout()
