from .base import Module
import random


class Hema(Module):
    DESCRIPTION = "Ribbit"
    MAX_RIBBITS = 500

    def response(self, query, message):
        try:
            repetitions = int(query)
            repetitions = min(repetitions, self.MAX_RIBBITS)
        except ValueError:
            repetitions = random.randint(5, 30)
        return " ".join(["ribbit"] * repetitions)
