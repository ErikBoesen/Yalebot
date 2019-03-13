from .base import Module
import requests

class FunFact(Module):
    DESCRIPTION = "Learn a fun fact"
    facts = []

    def fill_queue(self):
        raw = requests.get("http://mentalfloss.com/api/facts?page=4&limit=1").json()
        self.facts = [entry["fact"] for entry in raw]

    def response(self, query, message):
        if len(self.facts) == 0:
            self.fill_queue()
        return self.facts.pop()
