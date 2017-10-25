import liveplaylist as lp
import logging

test_url = ("https://www.setlist.fm/setlist/all-them-witches/2017/antones-austin-tx-1be7ed34.html")

# logging.basicConfig(level="INFO")
# gp = lp.gpmaa_playlist(test_url)
# gp.api.logout()
# gp.print_results()

setlist = lp.Setlist(test_url)
print(setlist)