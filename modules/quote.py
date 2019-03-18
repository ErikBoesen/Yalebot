from .base import Module
import requests


class Quote(Module):
    DESCRIPTION = "Generate inspirational quotes"

    def response(self, query, message):
        return requests.get("https://inspirobot.me/api?generate=true").text
