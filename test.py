import liveplaylist as lp
import logging

logging.basicConfig(level=logging.DEBUG)

test_url = ("https://www.setlist.fm/setlist/all-them-witches/2017/antones-austin-tx-1be7ed34.html")

setlist = lp.Setlist(test_url)
print(setlist)

p = lp.gpmaa_playlist(test_url)
