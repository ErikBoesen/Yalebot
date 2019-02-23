from .base import Module
import requests
from bs4 import BeautifulSoup

ENDPOINT = 'https://search.azlyrics.com/search.php?q='

class Lyrics(Module):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:67.0) Gecko/20100101 Firefox/67.0',
    }
    def response(self, query, message):
        song_name = query
        r = requests.get(ENDPOINT + song_name.replace(' ', '+'), headers=self.headers)
        bs = BeautifulSoup(r.text, 'html.parser')
        link = bs.find('div', {'class': 'panel'}).find('a')
        r = requests.get(link['href'], headers=self.headers)
        print(r.text)
        bs = BeautifulSoup(r.text, 'html.parser')
        column = bs.find('div', {'class': 'col-xs-12 col-lg-8 text-center'})
        divs = column.find_all('div', recursive=False)
        text = column.find('b', recursive=False).text
        text += divs[4].text
        return text
