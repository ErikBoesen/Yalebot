from .base import Module
from yaledining import YaleDining


class Dining(Module):
    DESCRIPTION = "Get information about Yale Dining services, closures, menus, etc."
    api = YaleDining()
    type_emoji = {
        "Residential": "🏠",
        "Retail": "💰",
    }

    def get_managers(self, location):
        managers = []
        num_managers = 0
        while num_managers < 4:
            num_managers += 1
            manager = (location[f"MANAGER{num_managers}NAME"],
                       location[f"MANAGER{num_managers}EMAIL"])
            if manager == (None, None):
                break
            managers.append(manager)
        return ", ".join([f"{name} ({email})" for name, email in managers])

    def capacity_bar(capacity: int):
        return ('▇' * capacity) + ('░' * (10 - capacity))

    def response(self, query, message):
        locations = self.api.get_locations()
        response = ""
        if query:
            desired_location = None
            for location in locations:
                if query == location["DININGLOCATIONNAME"]:
                    desired_location = location
            if desired_location is None:
                return("Unknown location name.")
            response += "-" * 3 + desired_location["DININGLOCATIONNAME"] + "-" * 3 + "\n"
            # TODO: repetition
            is_open = not bool(location["ISCLOSED"])
            # TODO: this sucks lol
            response += "Open: " + "Yes" if is_open else "No" + "\n"
            if is_open:
                response += "Capacity: {capacity}% ".format(capacity=location["CAPACITY"] * 10) + self.capacity_bar(is_open, location["CAPACITY"]) + "\n"
            response += "Type: " + location["TYPE"] + " " + self.type_emoji[location["TYPE"]] + "\n"
            response += "Address: " + "{address} ({coordinates})\n".format(address=location["ADDRESS"],
                                                                           coordinates=location["GEOLOCATION"])
            response += "Phone: " + location["PHONE"] + "\n"
            response += "Managers: " + self.get_managers(location) + "\n"
            menus = self.api.get_menus(desired_location["ID_LOCATION"])
            response += "\n" * 2
            if menus:
                response += "Menu support coming soon!"
            else:
                response += "No menu is currently available."
        else:
            for location in locations:
                is_open = not bool(location["ISCLOSED"])
                response += "- {emoji} {name} ({status})\n".format(emoji=self.type_emoji[location["TYPE"]],
                                                                   name=location["DININGLOCATIONNAME"],
                                                                   status="Open, {capacity}%".format(capacity=10 * location["CAPACITY"])
                                                                   if is_open else "Closed")
        return response
