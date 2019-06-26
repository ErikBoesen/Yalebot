from .base import Module
from yalebuildings import YaleBuildings
import os


class Building(Module):
    DESCRIPTION = "Get information on a building from Yale's campus, simply by specifying its ID"
    ARGC = 1
    api = YaleBuildings(os.environ.get("YALE_API_KEY"))

    def response(self, query, message):
        building = self.api.building(query)
        if building is None:
            return "No building found with that ID."
        return self.bullet_list(("Building " + building.id, building.name),
                                ("Category", building.category),
                                ("Address", building.address_1),
                                ("City", building.address_2),
                                ("Zip code", building.address_3),
                                ("Coordinates", f"({building.latitude}, {building.longitude})" if building.longitude and building.latitude else None),
                                ("Historical name", building.historical_name),
                                ("Fun facts", building.fun_facts))
