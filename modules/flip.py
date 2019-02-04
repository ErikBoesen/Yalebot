import upsidedown

class Flip:
    def response(self, query):
        return upsidedown.transform(query)
