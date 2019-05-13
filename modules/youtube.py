from .base import Module
import requests
from bs4 import BeautifulSoup


class YouTube(Module):
    DESCRIPTION = "Searches and sends YouTube video"
    ARGC = 1

    def response(self, query, message):
        search_url = "https://www.youtube.com/results?search_query="
        bs = BeautifulSoup(requests.get(search_url + query.replace(" ", "+").lower()).text, "html.parser")
        for link in bs.find_all("a"):
            path = link.get("href")
            if path.startswith("/watch"):
                return "https://www.youtube.com" + path
        return "No video found."
