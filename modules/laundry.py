from .base import Module
from yalelaundry import YaleLaundry
import os


class Laundry(Module):
    DESCRIPTION = "Get information about Yale's laundry rooms"
    api = YaleLaundry(os.environ.get("YALE_API_KEY"))

    def response(self, query, message):
        if query:
            pass
        else:
            rooms = self.api.rooms()
            items = []
            for room in rooms:
                avail = room.availability
                total = room.totals
                items.append((room.name,
                              f"{avail.washer}/{total.washer} washers, {avail.dryer}/{total.dryer} dryers currently available"))
            return self.bullet_list(items)
