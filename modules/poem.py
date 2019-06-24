from .base import Module
import random
import sys


class Poem(Module):
    DESCRIPTION = "Generate poetry"

    def __init__(self):
        super().__init__()
        self.poems = open("resources/poetry.txt", "r").read()
        self.poems = ''.join([i for i in self.poems if not i.isdigit()]).replace("\n\n", " ").split(' ')
        # This process the list of poems. Double line breaks separate poems, so they are removed.
        # Splitting along spaces creates a list of all words.

    def response(self, query, message):
        index = 1
        chain = {}

        count = 100 # Desired word count of output

        # This loop creates a dicitonary called "chain". Each key is a word, and the value of each key
        # is an array of the words that immediately followed it.
        for word in self.poems[index:]:
            key = self.poems[index - 1]
            if key in chain:
                chain[key].append(word)
            else:
                chain[key] = [word]
            index += 1

        word1 = random.choice(list(chain.keys())) #random first word
        message = word1.capitalize()

        # Picks the next word over and over until word count achieved
        while len(message.split(' ')) < count:
            word2 = random.choice(chain[word1])
            word1 = word2
            message += ' ' + word2

        return message
