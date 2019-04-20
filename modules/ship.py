from .base import Module
import requests
import random


class Ship(Module):
    DESCRIPTION = "Save thinking time when generating names for your new favorite hypothetical couples"
    ARGC = 1
    ENDPOINT = "https://couplenamegenerator.com/combine"

    def response(self, query, message):
        names = query.split()
        if len(names) != 2:
            return "Please provide two names."
        result = requests.post(self.ENDPOINT, data={"a1": names[0], "a2": names[1].lower()}).json()
        result += requests.post(self.ENDPOINT, data={"a1": names[1], "a2": names[0].lower()}).json()
        random.shuffle(result)
        return ", ".join(result)
