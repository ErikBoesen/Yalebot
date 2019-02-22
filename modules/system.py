from .base import Module
import re

class System(Module):
    pass

class Welcome(System):
    RE = re.compile(r'(.+) added (.+) to the group\.|(.+) has (re)?joined the group')
    def response(self):
        return "Welcome! I'm Yalebot, a helpful tool for the Yale GroupMe. Type !help to see what I can do."

    def get_name(self, query: str) -> str:
        """
        Get the name of the user described in the message.
        :param query: message text to parse.
        """
        # TODO: Clean up this logic
        results = self.RE.findall(query)
        results = [result for result in results if result not in ("", "re")]
        return results.pop()
