from .base import Module

import os
import requests
import json


class CleverBot:
    def __init__(self, user, key):
        self.user = user
        self.key = key
        self.nick = "Yalebot"

        body = {
            'user': user,
            'key': key,
            'nick': self.nick
        }
        requests.post('https://cleverbot.io/1.0/create', data=body)

    def query(self, text):
        body = {
            'user': self.user,
            'key': self.key,
            'nick': self.nick,
            'text': text
        }

        r = requests.post('https://cleverbot.io/1.0/ask', data=body)
        r = json.loads(r.text)

        if r['status'] == 'success':
            return r['response']
        else:
            return None


class Chat(Module):
    DESCRIPTION = "Converse with Yalebot intelligently"
    ARGC = 1
    def __init__(self):
        self.client = CleverBot(user=os.environ["CLEVERBOT_USER"], key=os.environ["CLEVERBOT_KEY"])
        super().__init__()

    def response(self, query, message):
        return self.client.query(query)
