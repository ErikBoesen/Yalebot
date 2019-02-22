from .base import Module
import re

class System(Module):
    pass

class Welcome(System):
    RE = re.compile(r'(.+) added (.+) to the group\.|(.+) has (re)?joined the group')
    def response(self):
        return "Welcome! I'm Yalebot, a helpful tool for the Yale GroupMe. Type !help to see what I can do."
    def get_user(self, query):
        """
        Get the name of the user described in the message.
        :param query: message text to parse.
        """
        names = self.RE.findall(query)
