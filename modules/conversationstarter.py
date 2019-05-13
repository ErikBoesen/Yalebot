from .base import Module
import requests


class ConversationStarter(Module):
    DESCRIPTION = "Generate an icebreaker question"
    responses = []
    
    def fill_queue(self):
        for x in range(10):
            question = requests.post("https://www.conversationstarters.com/random.php").text
            self.responses.append(question[39:])

    def response(self, query, message):
        if len(self.responses) == 0:
            self.fill_queue()
        return self.responses.pop()
