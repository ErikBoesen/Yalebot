from .base import Module

TEMPLATE = """%s wants to:

📍 Know your location"""

class Location(Module):
    def response(self, query, message):
        return TEMPLATE % query
