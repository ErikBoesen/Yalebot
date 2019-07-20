from .base import Module
import requests
from bs4 import BeautifulSoup
import random


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
        paragraph = str(bs.body.find("p", recursive=False))
        entries = paragraph.split("<br/>")
        # Remove informational content at the bottom of the paragraph
        entries.pop()
        # Remove opening <p> tag
        entries[0] = entries[0].replace("<p>", "")
        entries = [entry.strip() for entry in entries if not any([c in entry for c in ("-", ".")])]
        random.shuffle(entries)
        return ", ".join(entries)
