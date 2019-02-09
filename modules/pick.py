from .base import Module
import random
from groupy.client import Client

GROUP_ID = 46649296
TOKEN = client = Client.from_token(os.environ['GROUPME_ACCESS_TOKEN'])
group = client.groups.get(id=GROUP_ID)

class Pick(Module):
    DESCRIPTION = "Choose a person from a comma-separated list"
    def response(self, query):
        victim = random.choice(group.members)
        victim.remove()
        return "Bang"
