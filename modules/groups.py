from .base import Module


class Groups(Module):
    DESCRIPTION = "Get links to other admit groups"
    links = {
        "Yale University": "46649296/URP6KiXC",
        "University of Michigan": "46781389/hZehS1",
        "UNC Chapel Hill": "47712261/2K9zx7",
        "University of Virginia": "47680748/aLDXS1",
        "University of Miami": "48024399/XOwVQLZQ",
        "Baylor University": "42341652/aTexzNBA",
        "Virginia Tech": "46663109/rzmWS4",
        "University of Pennsylvania": "46633207/jo1Mk4wv",
        "Cornell University": "46579394/HJFvEV",
        "Liberty University": "49189743/Gjq3rDJX",
    }

    def response(self, query, message):
        return '\n'.join(["%s -> https://groupme.com/join_group/%s" % (name, self.links[name]) for name in self.links])
