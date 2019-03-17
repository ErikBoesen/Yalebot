from .base import Module
from imdb import IMDb

class Jake(Module):
    def __init__(self):
        super().__init__()
        self.imdb = IMDb()

    def response(self, query, message):
        if len(self.musicals) == 0:
            print(self.imdb.
