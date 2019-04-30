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
        a = soup.find_all("a")[22]
        href = a.get("href")
        # If no results are found, send recommendation
        if "/search?" in href:
            return f"No results found. Did you mean '{a.text}'?"
            # TODO: Use recursion to get that result automatically
        return "https://news.yale.edu" + href
