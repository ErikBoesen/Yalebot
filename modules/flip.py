from .base import Module
import upsidedown

class Flip(Module):
    DESCRIPTION = "Flip text over"
    def response(self, query, message):
        return upsidedown.transform(query)
