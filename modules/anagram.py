from .base import Module
import requests
from bs4 import BeautifulSoup


class Anagram(Module):
    DESCRIPTION = "Generate anagrams"
    ARGC = 1

    def response(self, query, message):
        html = requests.get("https://futureboy.us/lookup/nph-anagram.pl", params={"orig": query.replace(" ", "+"),
                                                                                  "list": 0,
                                                                                  "include": "",
                                                                                  "limit": 3,
                                                                                  "short": 3,
                                                                                  "cap": 1}).text
        bs = BeautifulSoup(html, "html.parser")
        paragraph = bs.find("p", recursive=False)
        print(paragraph)
