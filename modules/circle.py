from .base import Module
import requests
import random


class Circle(Module):
    DESCRIPTION = "Generate a compliment circle"

    def response(self, query, message):
        group_id = message["group_id"]
        users = requests.get(f"https://api.groupme.com/v3/groups/{group_id}?token={self.ACCESS_TOKEN}").json()["response"]["members"]
        users = [user["name"] for user in users]
        random.shuffle(users)
        return "".join([name + " -> " for name in users]) + users[0]
