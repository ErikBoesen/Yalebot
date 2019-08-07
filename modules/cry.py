from .base import Module
import random


class Cry(Module):
    DESCRIPTION = "Choose a place to cry, inspired by the \"Yale places i've cried\" Facebook group"

    PREPOSITIONS = (
        "inside", "outside", "in", "by", "near", "close to", "on top of", "atop",
    )
    ARTICLES = (
        "the", "every",
    )
    SUBLOCATIONS = (
        "library", "buttery", "courtyard", "roof", "bench", "statue of a dead white man", "statue",
    )
    OF = (
        "at",
    )
    LOCATIONS = [
        "the Yale Bowl",
        "Sterling memorial library",
        "the Beinecke Rare Book & Manuscript Library",
        "the Yale School of Forestry",
        "the Yale School of Art",
        "Yale Divinity School",
        "old campus",
        "Harkness Tower",
        "the Yale Center for British Art",
        "Bass Library",
        "Skull and Key Tomb",
        "the Yale Peabody Museum of Natural History",
        "the Yale Admissions Office",
    ] + [college + " residential college" for college in Module.COLLEGES]
    WITH = (
        "your froco", "your dus", "your suitemates", "the entire class of 2023", "yourself", "your roommate",
        "the Skull & Bones club", "the staff of the Yale Office of Career Strategy", "the Yale Admissions staff",
        "President Peter Salovey", "Yale College Dean Marvin Chun",
    )
    SENSITIVITY = True

    def response(self, query, message):
        text = ("Cry " + random.choice(self.PREPOSITIONS) + " " + random.choice(self.ARTICLES) + " " + random.choice(self.SUBLOCATIONS).upper() + " of " + random.choice(self.LOCATIONS).upper() + " with " + random.choice(self.WITH).upper())
        if self.SENSITIVITY:
            text += "\n\nPlease, if you are seriously in need of help, contact Yale Mental Health & Counseling. Call 203-432-0290 or visit yalewell.yale.edu/mental-health. 💙"
        return text
