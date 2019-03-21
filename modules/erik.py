from .base import Module


class Erik(Module):
    def response(self, query, message):
        return " ".join(query)
