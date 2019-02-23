from .base import Module
import requests
from bs4 import BeautifulSoup

ENDPOINT = 'https://www.lyricsfreak.com/search.php?q='

class Lyrics(Module):
    DESCRIPTION = 'Because Googling song titles is too hard sometimes'
    def response(self, query, message):
        song_name = query
        r = requests.get(ENDPOINT + song_name.replace(' ', '+'))
        bs = BeautifulSoup(r.text, 'html.parser')
        link = bs.find('a', {'class': 'song'})
        if link is None:
            return 'Could not find song "%s"' % song_name
        lyrics_page = 'https://www.lyricsfreak.com' + link['href']
        r = requests.get(lyrics_page)
        bs = BeautifulSoup(r.text, 'html.parser')
        column = bs.find('div', {'class': 'maincont d-cell al-t floatfix'})
        text = column.find('div', {'class': 'l_title'}).text.strip()
        text += '\n\n'
        text += column.find('div', {'id': 'content'}).text.strip()
        if len(text) > 1000:
            more = '...\n\nFull lyrics: ' + lyrics_page
            text = text[:1000-len(more)]
            text += more
        return text
