from .base import Module
import re


class RoomNumber(Module):
    DESCRIPTION = "Decode cryptic room numbers"
    ARGC = 1
    NUMBER = re.compile(r"^([A-Z]+)\d(\d+)([A-Z]+)?$")

    def verbalize_list(self, items):
        if len(items) > 1:
            last = items.pop()
            items[-1] += " and " + last
        return ", ".join(items)

    def response(self, query, message):
        # First letter is entryway
        # First number is floor number
        # Following number is the number of the room on that floor
        # A letter at the end is the room off the suite that you're in
        response = ""
        query = query.upper()
        if not self.NUMBER.match(query):
            return query + " is not a recognized room number."
        try:
            entryways = []
            while query[0].isalpha():
                entryways += query[0].upper()
                query = query[1:]
            response += "Your room can be accessed through the %s entryway%s.\n" % (self.verbalize_list(entryways),
                                                                                    "s" if len(entryways) > 1)
            floor = query[0]
            query = query[1:]
            response += "Your room is on floor #%s.\n" % floor
            room_number = ""
            while
