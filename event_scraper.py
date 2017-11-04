import html_fetch
import re
import datetime
from pprint import pprint

BASE_URL = 'https://www.bandsintown.com/cities/austin-tx?page='

def create_url(page=1):
    return BASE_URL + str(page)

def process_soup(soup):
    events = soup.select('tr[itemtype*=schema.org/MusicEvent]')
    processed = []
    for ev in events:
        event = {}
        event['date'] = datetime.datetime.strptime(ev.select_one('meta[itemprop*=startDate]')['content'], '%Y-%m-%d').date()
        event['artist'] = ev.select_one('.artist').text.strip()
        processed.append(event)
    return processed

def get_events(days_worth=1):
    page = 1
    events = []
    last_day = datetime.date.today() + datetime.timedelta(days=days_worth)
    while True:
        new = process_soup(html_fetch.create_soup(create_url(page)))
        fetch_count = len(new)
        new = [e for e in new if e['date'] < last_day]
        events += new
        page += 1
        if(len(new) != fetch_count):
            break
    return events
