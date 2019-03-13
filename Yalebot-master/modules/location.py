from .base import Module

TEMPLATE = """%s wants to:

📍 Know your location"""

class Location(Module):
    DESCRIPTION = "For when sending images is just too much work"
    ARGC = 1

    def response(self, query, message):
        return TEMPLATE % query
