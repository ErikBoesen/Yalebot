from .base import Module
import requests
from bs4 import BeautifulSoup

class Youtube(Module):
    DESCRIPTION = "Sends the first result on the YouTube search query"
    url = 'https://www.youtube.com/results?search_query='
    
    def response(self, query, message):
        url += query.replace(' ', '+').lower()
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        response = ''
        for link in soup.find_all('a'):
            result = link.get('href')
            if result.startswith('/watch'):
                response = result
                break
        return 'https://www.youtube.com' + response
