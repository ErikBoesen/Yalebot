from .base import Module
import requests
from bs4 import BeautifulSoup


class PDL(Module):
    DESCRIPTION = "Get a random comic from PoorlyDrawnLines.com, or give one by name"

    WEBSITE = "http://www.poorlydrawnlines.com/"

    def response(self, query, message):
        url = self.WEBSITE
        if query:
            url += "comic/" + query.lower().replace(" ", "-")
        content = requests.get(url).text
        page = BeautifulSoup(content, "html.parser")
        img = page.find("div", {"class": "post"}).find("img")
        return img["src"]
