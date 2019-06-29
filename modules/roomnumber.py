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
        if not query:
            return "Confidentially decode your room number using this helpful tool: https://erikboesen.com/roomnumbers"
        query = query.upper()

        result = self.NUMBER.search(query)
        if not result:
            return query + " is not a recognized suite or room."
        entryways, floor, suite, room = result.groups()
        response = (
            "Your suite can be accessed through entryway{pluralize_entryway} {entryways}, "
            "is on floor {floor}, and is suite #{suite} on that floor."
        ).format(pluralize_entryway="s" if len(entryways) > 1 else "",
                 entryways=self.verbalize_list(entryways),
                 floor=floor,
                 suite=suite)
        if room:
            response += " Your own room is room {room} within your suite.".format(room=room)
        return response
