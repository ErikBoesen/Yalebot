from .base import Module
from yalelaundry import YaleLaundry
import os


class Laundry(Module):
    DESCRIPTION = "Get information about Yale's laundry rooms"
    api = YaleLaundry(os.environ.get("YALE_API_KEY"))

    def response(self, query, message):
        if query:
            room = self.api.room(query)
            use = room.use
            items = [(room.name, f"({room.campus_name})")]
            items += [("Washers available", f"{use.available.washers}/{use.total.washers}"),
                      ("Dryers available", f"{use.available.dryers}/{use.total.dryers}")]
            for appliance in room.appliances:
                items.append((f"{appliance.type} {appliance.number}", appliance.time_remaining_raw))
            return self.bullet_list(items, embellish_first=True)
        else:
            rooms = self.api.rooms()
            items = []
            for room in rooms:
                use = room.use
                items.append((room.name,
                              f"{use.available.washers}/{use.total.washers} washers, {use.available.dryers}/{use.total.dryers} dryers currently available"))
            return self.bullet_list(items)
