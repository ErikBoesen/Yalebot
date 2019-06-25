from .base import Module
import random
import sys


class Poem(Module):
    DESCRIPTION = "Generate poetry"

    def __init__(self):
        super().__init__()
        with open("resources/poetry.txt", "r") as f:
            words = f.read().split()
        index = 1
        chain = {}
        # This loop creates a dicitonary called "chain". Each key is a word, and the value of each key
        # is an array of the words that immediately followed it.
        for word in self.poems[index:]:
            key = self.poems[index - 1]
            if key in chain:
                chain[key].append(word)
            else:
                chain[key] = [word]
            index += 1

    def response(self, query, message):
        first_word = random.choice(list(chain.keys()))
        message = first_word.capitalize()

        for _ in range(100):
            word = random.choice(chain[word])
            message += ' ' + word

        return message
