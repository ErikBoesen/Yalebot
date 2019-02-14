from .base import Module
import csv
import random

class Kelly(Module):
    DESCRIPTION = "Generate Elizabethan insults for our favorite person"
    primary_adjectives = []
    secondary_adjectives = []
    nouns = []
    def __init__(self):
        super().__init__()
        with open("resources/insults.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                self.primary_adjectives.append(row[0])
                self.secondary_adjectives.append(row[1])
                self.nouns.append(row[2])

    def response(self, query=None, message=None):
        return "Thou {primary_adjective}, {secondary_adjective} {noun}!".format(primary_adjective=random.choice(self.primary_adjectives),
                                                                                secondary_adjective=random.choice(self.secondary_adjectives),
                                                                                noun=random.choice(self.nouns))
