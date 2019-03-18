from .base import Module
import requests


class XKCD(Module):
    DESCRIPTION = "View the most recent XKCD comic, or specify a comic by number"

    def response(self, query, message):
        comic = requests.get(f"http://xkcd.com/{query}/info.0.json" if query else "http://xkcd.com/info.0.json").json()
        return ["\"" + comic["alt"] + "\"",
                comic["img"]]
