from .base import Module


class LMGTFY(Module):
    DESCRIPTION = "Let me Google that for you"
    ARGC = 1

    def response(self, query, message):
        return "http://lmgtfy.com/?q=" + query.replace(" ", "+")
