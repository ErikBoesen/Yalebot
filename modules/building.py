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
        response = ""
        response += f"Building {building.id}: {building.name}\n"
        if building.category:
            response += f"Category: {building.category}\n"
        response += f"Address:\n\t{building.address_1}\n\t{building.address_2}\n\t{building.address_3}\n"
        if building.latitude and building.longitude:
            response += f"Coordinates: ({building.latitude}, {building.longitude})\n"
        if building.historical_name:
            response += f"Historical name: {building.historical_name}\n"
        if building.prose:
            response += f"Fun facts: {building.fun_facts}\n"
        return response
