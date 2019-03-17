from .base import Module
import re

class Dania(Module):
    NUMBER = re.compile(r"[-+]?([0-9]*[\.'\"][0-9]+|[0-9]+)")
    def response(self, query, message):
        return self.NUMBER.sub("4'10.5", query)
