from .base import Module
import requests
from bs4 import BeautifulSoup


class Anna(Module):
    DESCRIPTION = "Need to hide some unpleasant content from the chat? Do so while appreciating Russian realist literature"

    def response(self, query, message):
        if message.user_id not in ["41430499"]:
            return "You gotta be Erik."
        bs = BeautifulSoup(requests.get("http://www.gutenberg.org/files/1399/1399-h/1399-h.htm").text, "html.parser")
        for pre in bs.find_all("pre"):
            pre.decompose()
        return bs.get_text()
