from .base import Module
import requests


class FunFact(Module):
    DESCRIPTION = "Learn a fun fact"
    facts = []

    def fill_queue(self):
        raw = requests.get("http://mentalfloss.com/api/facts?page=4&limit=1").json()
        self.facts = [entry["fact"] for entry in raw]

    def strip_tags(self, text, tags: tuple):
        for tag in tags:
            text = text.replace("<" + tag + ">", "").replace("</" + tag + ">", "")
        return text

    def response(self, query, message):
        if len(self.facts) == 0:
            self.fill_queue()
        text = self.facts.pop()
        text = self.strip_tags(text, ("em", "i"))
        return text
