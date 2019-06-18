from .base import Module
from yaledining import YaleDining


class Dining(Module):
    DESCRIPTION = "Get information about Yale Dining services, closures, menus, etc."
    api = YaleDining()
    type_emoji = {
        "Residential": "🏠",
        "Retail": "💰",
    }

    def capacity_bar(self, capacity: int):
        return ('▇' * capacity) + ('░' * (10 - capacity))

    def response(self, query, message):
        response = ""
        if query:
            location = self.api.location(name=query)
            if location is None:
                return f"Unknown location name '{query}'."
            response += ("-" * 3) + location.name + ("-" * 3) + "\n"
            response += "Open: " + ("Yes" if location.open else "No") + "\n"
            if location.open:
                response += "Capacity: {capacity}% ".format(capacity=location.percent_capacity) + self.capacity_bar(location.percent_capacity) + "\n"
            response += "Type: " + location.type + " " + self.type_emoji[location.type] + "\n"
            response += "Address: " + "{address} ({coordinates})\n".format(address=location.address,
                                                                           coordinates=location.geolocation)
            response += "Phone: " + location.phone + "\n"
            response += "Managers: " + ", ".join([f"{manager.name} ({manager.email})" for manager in location.managers]) + "\n"
            menus = location.menus
            response += "\n"
            if menus:
                response += "Menu support coming soon!"
            else:
                response += "No menu is currently available."
        else:
            locations = self.api.locations()
            for location in locations:
                response += "- {emoji} {name} ({status})\n".format(emoji=self.type_emoji[location.type],
                                                                   name=location.name,
                                                                   status=("Open" + ((", {capacity}% capacity".format(capacity=location.percent_capacity) + self.capacity_bar(location.capacity)) if location.capacity is not None else "")) if location.open else "Closed")
        return response
