from .base import Module

BOOLA_BOOLA = """Bulldog!  Bulldog!
Bow, wow, wow
Eli Yale
Bulldog!  Bulldog!
Bow, wow, wow
Our team can never fail

When the sons of Eli
Break through the line
That is the sign we hail
Bulldog!  Bulldog!
Bow, wow, wow
Eli Yale!"""

class Bulldog(Module):
    DESCRIPTION = "Sing everybody's favorite song!"
    def response(self, query):
        return BOOLA_BOOLA
