from .base import Module
from bs4 import BeautifulSoup
import requests
import random


class Jake(Module):
    DESCRIPTION = "If it's on a stage, it's a musical"
    musicals = []

    def __init__(self):
        super().__init__()

    def response(self, query, message):
        if len(self.musicals) == 0:
            bs = BeautifulSoup(requests.get("https://www.imdb.com/list/ls000071646/").text, 'html.parser')
            musical_elements = bs.find("div", {"class": "lister-list"}).find_all("div", {"class": "lister-item"})
            for entry in musical_elements:
                self.musicals.append((entry.find("h3", {"class": "lister-item-header"}).find("a", recursive=False).text,
                                      entry.find_all("p")[1].text.strip()))
        title, description = random.choice(self.musicals)
        return f"{title}: {description}"
