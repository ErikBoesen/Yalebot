from .base import Module
import requests


class ConversationStarter(Module):
    DESCRIPTION = "Generate an icebreaker question"

    def response(self, query, message):
        question = requests.post("https://www.conversationstarters.com/random.php").text
        # Trim off <img> tag from start
        question = question[39:]
        return question
