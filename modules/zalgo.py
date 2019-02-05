from .base import Module
import zalgoify

class Zalgo(Module):
    def response(self, query):
        return zalgoify.process(query)
