from .base import Module


class Maria(Module):
    DESCRIPTION = "Mdl fr Mr's hmwrk"

    def response(self, query, message):
        return "".join([character for character in query if character.lower() not in ("a", "b", "c", "d", "e")])
