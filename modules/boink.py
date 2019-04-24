from .base import Module
import requests
import random
import re


class Boink(Module):
    DESCRIPTION = "Make a match"
    queues = {}

    def get_mention(self, query):
        """
        Find the name of anyone mentioned in message.
        """
        match = re.search(r'@.+', query)
        if match:
            return match.group().lstrip('@')

    def response(self, query, message):
        group_id = message["group_id"]
        if self.queues.get(group_id) is None or len(self.queues[group_id]) < 2:
            users = requests.get(f"https://api.groupme.com/v3/groups/{group_id}?token={self.ACCESS_TOKEN}").json()["response"]["members"]
            self.queues[group_id] = [user["name"] for user in users]
            random.shuffle(self.queues[group_id])
        mention = self.get_mention(query)
        name1 = mention or self.queues[group_id].pop()
        name2 = self.queues[group_id].pop()
        return f"I choose... {name1} & {name2}! 💙"
