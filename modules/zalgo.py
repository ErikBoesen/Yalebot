from .base import Module
import zalgoify


class Zalgo(Module):
    DESCRIPTION = "HE IS COMING"
    def response(self, query, message):
        return zalgoify.process(query)
