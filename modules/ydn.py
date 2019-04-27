from .base import Module
import requests
from bs4 import BeautifulSoup
import random


class YDN(Module):
    DESCRIPTION = "Get news from the Yale Daily News"
    url = 'https://news.yale.edu/news-rss'
    def response(self, query, message):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return random.choice(list(map(lambda x: x.get_text(), soup.find_all("guid"))))
