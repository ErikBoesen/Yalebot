from .base import Module
import requests
import re

class FunFact(Module):
    DESCRIPTION = "Learn a fun fact"
    facts = []

    def fill_queue(self):
        raw = requests.get("http://mentalfloss.com/api/facts?page=4&limit=1").json()
        self.facts = [entry["fact"] for entry in raw]

    def response(self, query, message):
        if len(self.facts) == 0:
            self.fill_queue()
        raw_text = self.facts.pop()
        cleanr = re.compile('<.*?>')
        clean_text = re.sub(cleanr, '', raw_text)
        return clean_text
