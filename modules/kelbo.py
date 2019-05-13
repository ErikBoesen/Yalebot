from .base import Module
import random
from random_word import RandomWords
import time


class Kelbo(Module):
    DESCRIPTION = '____ __ _____'
    ARGC = 0
    dictionary = RandomWords()

    def random(self):
        """
        :return: random string of underscores separated by spaces
        """
        return " ".join(["_" * random.randint(1, 5) for _ in range(random.randint(2, 10))])

    def kelboify(self, text):
        """
        :param text: text to convert to underscores
        :return: converted text
        """
        return "".join([" " if char == " " else "_" for char in text])

    def get_word(self, length):
        while True:
            try:
                return self.dictionary.get_random_word(minLength=length, maxLength=length)
            except Exception:
                pass
            time.sleep(1)

    def response(self, query, message):
        if "_" in query:
            results = []
            words = [self.get_word(len(underscores)) for underscores in query.split()]
            return " ".join(words)
        else:
            if len(query) > 0:
                return self.kelboify(query)
            else:
                return self.random()
