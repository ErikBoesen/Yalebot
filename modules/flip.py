from .base import Module
import upsidedown

class Flip(Module):
    DESCRIPTION = "Flip text over"
    def response(self, query):
        return upsidedown.transform(query)
