from .base import Module
from yaledining import API


class Dining(Module):
    DESCRIPTION = "Get information about Yale Dining services, closures, menus, etc."
    api = API()

    def occupancy_bar(self, occupancy: int):
        return ('▇' * occupancy) + ('░' * (10 - occupancy))

    def response(self, query, message):
        response = ""
        halls = self.api.halls()
        halls = [hall for hall in halls if hall.open]
        if halls:
            for hall in halls:
                response += "- {name} ({status})\n".format(name=hall.name,
                                                                   status=("{occupancy}% occupancy ".format(occupancy=hall.occupancy * 10) + self.occupancy_bar(hall.occupancy)) if hall.occupancy is not None else "Open")
        else:
            response = "No dining halls are currently open."
        response += "\nDownload Yale Menus at https://yalemenus.com to view full menus."
        return response
