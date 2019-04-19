from .base import Module
import requests


class Ship(Module):
    ARGC = 1

    def response(self, query, message):
        names = query.split()
        if len(names) != 2:
            return "Please provide two names."
        result = requests.post("https://couplenamegenerator.com/combine", data={"a1": names[0], "a2": names[1]}).json()
        return ", ".join(result)

