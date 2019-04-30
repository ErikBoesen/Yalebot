from .base import Module
import requests
from bs4 import BeautifulSoup


class YDN(Module):
    DESCRIPTION = 'Search for a news article on the Yale Daily News'
    ARGC = 1
    def response(self, query, message):
        url = f'https://news.yale.edu/search?sort=created&order=desc&search_api_views_fulltext={query.replace(" ", "%20").lower()}'
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        link = list(map(lambda x: x.get("href"), soup.find_all("a")))[22]
        # if typo comes up, searches the suggested keyword 
        if '/search?' in link:
            soup = BeautifulSoup(requests.get(f'https://news.yale.edu{link}').text, 'html.parser')
            link = list(map(lambda x: x.get("href"), soup.find_all("a")))[22]
        return f'https://news.yale.edu{link}'
