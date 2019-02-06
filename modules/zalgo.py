from .base import Module
import zalgoify


class Zalgo(Module):
    DESCRIPTION = "HE IS COMING"
    def response(self, query):
        return zalgoify.process(query)
