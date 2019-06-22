from .base import Module

TEMPLATE = """>
i am:
⚪️ male
⚪️ female
🔘 %s
"""


class IAm(Module):
    DESCRIPTION = "Create an 'I am:' radio button tweet"
    ARGC = 1

    def response(self, query, message):
        return TEMPLATE % query
