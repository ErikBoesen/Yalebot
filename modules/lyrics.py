from .base import Module
import requests
from bs4 import BeautifulSoup

ENDPOINT = 'https://www.lyricsfreak.com/search.php?q='

class Lyrics(Module):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:67.0) Gecko/20100101 Firefox/67.0',
    }
    def response(self, query, message):
        song_name = query
        r = requests.get(ENDPOINT + song_name.replace(' ', '+'), headers=self.headers)
        bs = BeautifulSoup(r.text, 'html.parser')
        link = bs.find('a', {'class': 'song'})
        r = requests.get('https://www.lyricsfreak.com' + link['href'], headers=self.headers)
        bs = BeautifulSoup(r.text, 'html.parser')
        column = bs.find('div', {'class': 'maincont d-cell al-t floatfix'})
        text = column.find('div', {'class': 'l_title'}).text.strip()
        text += '\n' + '-' * 20 + '\n\n'
        text += column.find('div', {'id': 'content'}).text.strip()
        return text
