from .base import Module
import requests
from bs4 import BeautifulSoup


class YouTube(Module):
    DESCRIPTION = "Searches and sends YouTube video"
    ARGC = 1

    def response(self, query, message):
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '%20').lower()}"
        bs = BeautifulSoup(requests.get(url).text, "html.parser")
        return f"https://www.youtube.com{list(map(lambda x: x.get("href"), bs.find_all("a")))[44]}"
