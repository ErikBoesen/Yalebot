from .base import Module
import os
import requests
import json


class CleverBot:
    def __init__(self, user, key, group_id):
        self.user = user
        self.key = key
        self.nick = f"Yalebot_{group_id}"

        body = {
            "user": user,
            "key": key,
            "nick": self.nick
        }
        requests.post("https://cleverbot.io/1.0/create", data=body)

    def query(self, text):
        body = {
            "user": self.user,
            "key": self.key,
            "nick": self.nick,
            "text": text
        }

        r = requests.post("https://cleverbot.io/1.0/ask", data=body)
        r = json.loads(r.text)

        if r["status"] == "success":
            return r["response"]
        else:
            return None


class Chat(Module):
    DESCRIPTION = "Converse with Yalebot intelligently"
    ARGC = 1
    clients = {}

    def __init__(self):
        super().__init__()

    def response(self, query, message):
        group_id = message["group_id"]
        if self.clients.get(group_id) is None:
            self.clients[group_id] = CleverBot(os.environ.get("CLEVERBOT_USER"), os.environ.get("CLEVERBOT_KEY"), group_id)
        return self.clients[group_id].query(query)
