from .base import Module
import requests
from bs4 import BeautifulSoup
import random


class Dog(Module):
    DESCRIPTION = "Learn about a pupper"
    dogs = []
    def __init__(self):
        super().__init__()
        r = requests.get("https://en.wikipedia.org/wiki/List_of_individual_dogs")
        bs = BeautifulSoup(r.text, "html.parser")
        lists = bs.find("div", {"class": "mw-parser-output"}).find_all("ul", recursive=False)
        for ul in lists:
            self.dogs += [BeautifulSoup(str(li), "html.parser").text for li in ul]

    def response(self, query, message):
        return random.choice(self.dogs)
