from .base import Module
import requests
from bs4 import BeautifulSoup


class YouTube(Module):
    DESCRIPTION = "Searches and sends YouTube video"
    ARGC = 1

    def response(self, query, message):
        url = "https://www.youtube.com/results?search_query=" + query.replace(" ", "+")
        bs = BeautifulSoup(requests.get(url).text, "html.parser")
        link = bs.find_all("a")[44]["href"]
        return "https://www.youtube.com" + link
