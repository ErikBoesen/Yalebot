from .base import Module
import random

class Kelbo(Module):
    DESCRIPTION = '____ __ _____'
    ARGC = 0

    def random(self):
        """
        :return: random string of underscores separated by spaces
        """
        return " ".join(["_" * random.randint(1, 5) for _ in range(random.randint(2, 10)])

    def kelboify(self, text):
        """
        :param text: text to convert to underscores
        :return: converted text
        """
        return "".join([" " if char == " " else "_" for char in text])

    def response(self, query, message):
        if len(query) > 0:
            return self.kelboify(query)
        else:
            return self.random()
