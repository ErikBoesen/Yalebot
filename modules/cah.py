from .base import Module


class CardsAgainstHumanity(Module):
    DESCRIPTION = "Play everyone's favorite card game for terrible people."

    def response(self, query, message):
        command, query = query.split(None, 1)
