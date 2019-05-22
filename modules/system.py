from .base import Module
import re
import random


class System(Module):
    def get_names_groupme(self, query: str) -> str:
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
        return results.pop().replace(" and ", ", ").split(", ")


class Welcome(System):
    RE = re.compile(r"(.+) added (.+) to the group\.|(.+) has (re)?joined the group")

    def response(self, query, message):
        names = [name.split(" ", 1)[0] for name in self.get_names_groupme(query)]
        # Join names list together
        if len(names) > 1:
            last = names.pop()
            names[-1] += ("," if len(names) > 2 else "") + " and " + last
        names = ", ".join(names)
        return self.wave() + " Welcome " + names + "! We're happy to have you. I'm Yalebot, a GroupMe bot for Yale University. Type !help to see what I can do."


class Mourn(System):
    RE = re.compile(r"(.+) has left the group\.|(.+) removed (.+) from the group\.")

    def response(self, query, message):
        return random.choice(["Farewell, sweet prince",
                              "You hear that? That's the sound of someone committing elsewhere."])


class Introduce(System):
    RE = re.compile(r"(.+) added the Yalebot.* bot.")

    def response(self, query, message):
        return self.wave() + " Hi! I'm Yalebot. Thanks for adding me. Type !help to see what I can do."
