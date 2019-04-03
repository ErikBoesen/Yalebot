from .base import Module
import random
import string


class Renee(Module):
    DESCRIPTION = "Go both crazy and stupid"

    def response(self, query, message):
        return "".join([random.choice(string.ascii_letters) for _ in range(0, random.randint(50, 100))]) + "!!!"
