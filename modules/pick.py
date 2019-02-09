from .base import Module
import random

class Pick(Module):
    DESCRIPTION = "Choose a random person to kill"
    def response(self, query):
        options = [name.strip() for name in query.split(',')]
        return "Thinking...\n\nI choose...\n\n" + random.choice(options) + "!"
