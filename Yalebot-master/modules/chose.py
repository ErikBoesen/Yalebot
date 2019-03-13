from .base import Module
import random

class Chose(Module):
    DESCRIPTION = "Sing our other favorite song"
    def response(self, query, message):
        return "Bum" + " bum" * random.randint(0, 30) + ", that's why I chose Y" + "a" * random.randint(0, 30) + "le! https://www.youtube.com/watch?v=tGn3-RW8Ajk"
