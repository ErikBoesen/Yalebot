from .base import Module
import requests
from bs4 import BeautifulSoup
import random
import re


class Dog(Module):
    DESCRIPTION = "Get learned about a pupper"
    dogs = []
    CITATION = re.compile(r'\[\d+\]')
    def __init__(self):
        super().__init__()
        r = requests.get("https://en.wikipedia.org/wiki/List_of_individual_dogs")
        bs = BeautifulSoup(r.text, "html.parser")
        lists = bs.find("div", {"class": "mw-parser-output"}).find_all("ul", recursive=False)
        for ul in lists:
            self.dogs += [BeautifulSoup(str(li), "html.parser").text for li in ul]
        # Filter out empty items
        self.dogs = [self.CITATION.sub('', dog) for dog in self.dogs if len(dog) > 5]

    def response(self, query, message):
        return random.choice(self.dogs)
