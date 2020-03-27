from .base import Module


class Spaces(Module):
    DESCRIPTION = "s p a c e s"
    ARGC = 1

    def response(self, query, message):
        return " ".join(query)
