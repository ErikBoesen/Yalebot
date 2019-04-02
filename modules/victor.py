from .base import Module
import requests
from bs4 import BeautifulSoup
import random

class Victor(Module):
    DESCRIPTION = ""
    responses = []

    def response(self, query, message):
        if len(self.responses) == 0:
            url = "https://www.youtube.com/playlist?list=PLCDiziww_AU_JXjGIUfx7f69yxlDNMb3c"
            bs = BeautifulSoup(requests.get(url).text, "html.parser")
            for link in bs.find_all("a"):
                result = link.get("href")
                if result.startswith("/watch"):
                    self.responses.append("https://www.youtube.com" + result)
            random.shuffle(self.responses)
        return self.responses.pop()
