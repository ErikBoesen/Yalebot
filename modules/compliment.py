from .base import Module
import random


class Compliment(Module):
    DESCRIPTION = "Say something nice to someone"

    def __init__(self):
        super().__init__()
        with open("resources/compliments.txt") as f:
            self.compliments = f.readlines()

    def response(self, query, message):
        return ((query + ": ") if query else "") + random.choice(self.compliments).strip('\n')
