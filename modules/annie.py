from .base import Module


class Annie(Module):
    DESCRIPTION = "Give a nice round of applause"
    ARGC = 1
    CLAP = "👏"

    def response(self, query, message):
        return self.CLAP + query.replace(" ", self.CLAP) + self.CLAP
