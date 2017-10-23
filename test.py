import liveplaylist
import logging

test_url = ("https://www.setlist.fm/setlist/all-them-witches/2017/antones-austin-tx-1be7ed34.html")

# logging.basicConfig(level="INFO")
gp = liveplaylist.gpmaa_playlist(test_url)
gp.api.logout()
gp.print_results()