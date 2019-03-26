from .base import Module


class Maria(Module):
    DESCRIPTION = "Mdl fr Mr's hmwrk"
    ARGC = 1

    def response(self, query, message):
        return "".join([character for character in query if character.lower() not in "aeiouy"])
