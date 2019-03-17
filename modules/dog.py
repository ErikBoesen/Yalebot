from .base import Module
import requests
from bs4 import BeautifulSoup
import random
import re


class Dog(Module):
    DESCRIPTION = "Get learned about a pupper"
    dogs = []
    CITATION = re.compile(r'\[\d+\]')
    def response(self, query, message):
        if len(self.dogs) == 0:
            r = requests.get("https://en.wikipedia.org/wiki/List_of_individual_dogs")
            bs = BeautifulSoup(r.text, "html.parser")
            lists = bs.find("div", {"class": "mw-parser-output"}).find_all("ul", recursive=False)
            dogs = []
            for ul in lists:
                dogs += [BeautifulSoup(str(li), "html.parser").text for li in ul]
            # Filter out empty items and remove citations
            dogs = [self.CITATION.sub('', dog) for dog in self.dogs if len(dog) > 5]
            self.dogs = dogs
        return random.choice(self.dogs)
