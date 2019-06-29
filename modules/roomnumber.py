from .base import Module
import re


class RoomNumber(Module):
    DESCRIPTION = "Decode cryptic room numbers"
    ARGC = 1
    NUMBER = re.compile(r"^([A-Z]+)(\d)(\d+)([A-Z]+)?$")

    def verbalize_list(self, items):
        items = list(items)
        if len(items) > 1:
            last = items.pop()
            items[-1] += " and " + last
        return ", ".join(items)

    def response(self, query, message):
        # First letter is entryway
        # First number is floor number
        # Following number is the number of the room on that floor
        # A letter at the end is the room off the suite that you're in
        query = query.upper()

        result = self.NUMBER.search(query)
        if not result:
            return query + " is not a recognized suite or room."
        entryways, floor, suite, room = result.groups()
        response = ""
        response += "Your suite can be accessed through entryway%s %s, " % ("s" if len(entryways) > 1 else "",
                                                                            self.verbalize_list(entryways))
        response += "is on floor %s, and is suite #%s on that floor.\n" % (floor, room_number)
        if query:
            response += " Your own room is room %s in your suite.\n" % query
        return response
