import clever
import os

class Chat:
    def __init__(self):
        self.client = clever.CleverBot(user=os.environ["CLEVERBOT_USER"], key=os.environ["CLEVERBOT_KEY"])

    def response(self, query):
        return self.client.query(query)
