from .base import Module


class Crista(Module):
    DESCRIPTION = "s p a c e s"

    def response(self, query, message):
        return " ".join(query)
