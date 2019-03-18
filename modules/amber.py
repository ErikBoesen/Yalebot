from .base import Module
import random


class Amber(Module):
    DESCRIPTION = 'aMbEr'
    ARGC = 1

    def scramble(self, string):
        capitalize = bool(random.getrandbits(1))
        return string.capitalize() if capitalize else string.lower()

    def response(self, query, message):
        return ''.join([self.scramble(char) for char in query])
