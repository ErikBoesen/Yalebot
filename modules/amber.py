from .base import Module
import random

class Amber(Module):
    DESCRIPTION = 'aMbEr'
    def scramble(self, string):
        capitalize = bool(random.getrandbits(1))
        return string.capitalize() if capitalize else string

    def response(self, query, message):
        return ''.join([self.scramble(char) for char in query])
