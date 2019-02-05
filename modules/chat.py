import os
import requests
import json


class CleverBot(object):
    def __init__(self, user, key, nick=None):
        self.user = user
        self.key = key
        self.nick = nick

        body = {
            'user': user,
            'key': key,
            'nick': nick
        }
        requests.post('https://cleverbot.io/1.0/create', json=body)

    def query(self, text):
        body = {
            'user': self.user,
            'key': self.key,
            'nick': self.nick,
            'text': text
        }

        r = requests.post('https://cleverbot.io/1.0/ask', json=body)
        r = json.loads(r.text)

        if r['status'] == 'success':
            return r['response']
        else:
            return False


class Chat:
    def __init__(self):
        self.client = CleverBot(user=os.environ["CLEVERBOT_USER"], key=os.environ["CLEVERBOT_KEY"])

    def response(self, query):
        return self.client.query(query)
