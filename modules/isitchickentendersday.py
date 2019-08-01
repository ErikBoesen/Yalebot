from .base import Module
import requests


class IsItChickenTendersDay(Module):
    DESCRIPTION = "Well? Is it? Inspired by isitchickentendersday.com."

    def response(self, query, message):
        text = requests.get("http://www.isitchickentendersday.com/").text
        if "Yes" in text:
            return "Yes"
        if "No" in text:
            return "No"
        return "Who knows?"
