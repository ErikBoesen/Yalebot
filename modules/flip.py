from .base import Module
import upsidedown

class Flip(Module):
    def response(self, query):
        return upsidedown.transform(query)
