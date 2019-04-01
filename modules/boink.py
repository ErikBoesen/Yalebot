from .base import Module
import requests
import random


class Boink(Module):
    DESCRIPTION = "Make a match"

    def response(self, query, message):
        group_id = message["group_id"]
        users = requests.get(f"https://api.groupme.com/v3/groups/{group_id}?token={self.ACCESS_TOKEN}").json()["response"]["members"]
        users = [user["name"] for user in users]
        name1 = random.choice(users)
        name2 = random.choice(users)
        return f"I choose... {name1} & {name2}! 💙"
