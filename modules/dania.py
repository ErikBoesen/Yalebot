from .base import Module
import re

class Dania(Module):
    HEIGHT = "4'10.5"
    DESCRIPTION = HEIGHT
    ARGC = 1
    NUMBER = re.compile(r"[-+]?([0-9]*[\.'\"][0-9]+|[0-9]+)")
    def response(self, query, message):
        return self.NUMBER.sub(self.HEIGHT, query)
