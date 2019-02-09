from .base import Module
import random


class EightBall(Module):
    DESCRIPTION = "Predict the future or circumvent your own indecisiveness"
    OPTIONS = [
        "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.",
        "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
        "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
        "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."
    ]
    def response(self, query, message):
        #query_hash = sum([ord(character) for character in query])
        #return self.OPTIONS[query_hash % len(self.OPTIONS)]
        return random.choice(self.OPTIONS)
