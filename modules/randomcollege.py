from .base import Module
import random


class RandomCollege(Module):
    DESCRIPTION = "Choose a random college"
    COLLEGES = [
        'Benjamin Franklin',
        'Berkeley',
        'Branford',
        'Davenport',
        'Ezra Stiles',
        'Grace Hopper',
        'Jonathan Edwards',
        'Morse',
        'Pauli Murray',
        'Pierson',
        'Saybrook',
        'Silliman',
        'Timothy Dwight',
        'Trumbull',
    ]

    def response(self, query, message):
        return random.choice(self.COLLEGES)
