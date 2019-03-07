from .base import Module
import random

class Pick(Module):
    DESCRIPTION = "Choose from a comma-separated list"
    def response(self, query, message):
        options = [name.strip() for name in query.split(',')]
        return "Thinking...\n\nI choose...\n\n" + random.choice(options) + "!"
