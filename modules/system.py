from .base import Module
import re

class System(Module):
    pass

class Welcome(System):
    RE = re.compile(r'(.+) added (.+) to the group\.|(.+) has (re)?joined the group')
    def response(self):
        return "Welcome! We're happy to have you. Type !help to see what I can do."

    def get_names(self, query: str) -> str:
        """
        Get the name of the user described in the message.
        :param query: message text to parse.
        """
        # TODO: Clean up this logic for choosing the name of the joining/added user
        # This returns a list of tuples, each having the content of of the parenthesized groups
        results = self.RE.findall(query).pop()
        # Filter out empty groups and "re" (which would only be there if someone rejoined the group)
        results = [result for result in results if result not in ("", "re")]
        # Return the last non-empty (and non-re) match
        # Account for multiple users being added simultaneously, also
        return results.pop().split(" and ")
