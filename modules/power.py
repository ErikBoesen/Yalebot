from .base import Module
import random


class Power(Module):
    DESCRIPTION = "The POWER that that has"
    words = ["power", "intelligence", "clearance", "access", "influence", "profile", "international implications"]

    def response(self, query, message):
        return "The {word} that that has".format(word=random.choice(self.words).upper())
