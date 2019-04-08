from .base import Module


class Tiya(Module):
    DESCRIPTION = "DAMN"

    def indamnify(self, word):
        return word.upper() + "."

    def response(self, query, message):
        return " ".join([self.indamnify(word) for word in query.split(" ")])
