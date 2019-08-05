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
            location = self.api.location(query)
            if location is None:
                return f"Unknown location name '{query}'."
            response = self.bullet_list(((location.name, "Open" if location.is_open else "Closed"),
                                         ("Capacity", (f"{location.percent_capacity}% " + self.capacity_bar(location.capacity)) if location.is_open else None),
                                         ("Type", location.type + " " + self.type_emoji[location.type]),
                                         ("Address", f"{location.address} ({location.geolocation})"),
                                         ("Phone", location.phone),
                                         ("Managers", ", ".join([f"{manager.name} ({manager.email})" for manager in location.managers]))),
                                        embellish_first=True) + "\n"
            meals = location.meals
            if meals:
                response += self.bullet_list(tuple([(meal.date.strftime("%m/%d") + " " + meal.name,
                                                     ", ".join([item.name for item in meal.items])) for meal in meals]))
                for meal in meals:
                    response
            else:
                response += "No menu is currently listed."
        else:
            locations = self.api.locations()
            locations = [location for location in locations if location.is_open]
            if locations:
                for location in locations:
                    response += "- {emoji} {name} ({status})\n".format(emoji=self.type_emoji[location.type],
                                                                       name=location.name,
                                                                       status=("{capacity}% capacity ".format(capacity=location.percent_capacity) + self.capacity_bar(location.capacity)) if location.capacity is not None else "Open")
            else:
                response = "No dining locations are currently open."
        return response
