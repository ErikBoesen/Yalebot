from .base import Module
import requests

class XKCD(Module):
    def response(self, query, message):
        comic = requests.get("http://xkcd.com/{query}/info.0.json" if query else "http://xkcd.com/info.0.json").json()
        return "Hover text: \"" + comic['alt'] + "\n" + comic["img"]
