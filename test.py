import liveplaylist as lp
import logging

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)

test_url = ("https://www.setlist.fm/setlist/king-gizzard-and-the-lizard-wizard/2018/variety-playhouse-atlanta-ga-43eac383.html")

setlist = lp.Setlist(test_url)
print(setlist)

p = lp.gpmaa_playlist(test_url)
p.make_playlist()
p.api.logout()
