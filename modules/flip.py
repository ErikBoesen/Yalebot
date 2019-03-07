from .base import Module
import upsidedown

class Flip(Module):
    DESCRIPTION = "Flip text over"
    ARGC = 1
    def response(self, query, message):
        return upsidedown.transform(query)
