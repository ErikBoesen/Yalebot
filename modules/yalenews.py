from .base import Module
import requests
from bs4 import BeautifulSoup


class YaleNews(Module):
    DESCRIPTION = "Search for a news article on Yale News"
    ARGC = 1

    def response(self, query, message):
        url = "https://news.yale.edu/search?sort=created&order=desc&search_api_views_fulltext=" + query
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        # TODO: protect against exact link index being changed
        link = [link.get("href") for link in soup.find_all("a")][22]
        # if typo comes up, searches the suggested keyword
        if "/search?" in link:
            soup = BeautifulSoup(requests.get("https://news.yale.edu" + link).text, "html.parser")
            link = list(map(lambda x: x.get("href"), soup.find_all("a")))[22]
        return "https://news.yale.edu" + link
