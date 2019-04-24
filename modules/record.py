from .base import Module
import requests
from bs4 import BeautifulSoup


class Record(Module):
    DESCRIPTION = "Search for articles on the Yale Record, Yale's foremost satire magazine."
    ARGC = 1

    def response(self, query, message):
        r = requests.get("http://yalerecord.org/?s=" + query.replace(" ", "+"))
        bs = BeautifulSoup(r.text, "html.parser")
        return bs.find({"rel": "bookmark"}).href
