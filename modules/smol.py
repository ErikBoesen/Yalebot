from .base import Module


class Smol(Module):
    DESCRIPTION = "Make superscript text"
    ARGC = 1

    def __init__(self):
        with open("resources/superscript.txt", "r") as f:
            original, superscript = f.readlines()
        self.chars = {o: s for o, s in zip(original, superscript)}

    def response(self, query, message):
        return "".join([self.chars.get(c, c) for c in query])
