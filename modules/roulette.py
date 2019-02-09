from .base import Module
import random
from groupy.client import Client
import os

GROUP_ID = 46649296
TOKEN = client = Client.from_token(os.environ['GROUPME_ACCESS_TOKEN'])
group = client.groups.get(id=GROUP_ID)

class Roulette(Module):
    DESCRIPTION = "Choose a random person to kill"
    def response(self, query):
        if random.randint(1, 6) == 6:
            victim = random.choice(group.members)
            victim.remove()
            return "Bang"
        else:
            return "Click"
