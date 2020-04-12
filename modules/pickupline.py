from .base import Module
import requests
from bs4 import BeautifulSoup


class PickUpLine(Module):
    DESCRIPTION = "Say something nice to someone"

    def response(self, query, message):
        bs = BeautifulSoup(requests.get("http://pickuplinegen.com").text, "html.parser")
        content = bs.find(id="content")
        return content.text.strip()
