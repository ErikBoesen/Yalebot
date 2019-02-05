from .base import Module
import requests
import os

class Weather(Module):
    location_name = "New Haven, CT"
    location_coords = {
        "x": 41.3083,
        "y": -72.9279
    }

    def response(self, query):
        r = requests.get("https://api.weather.gov/points/{x},{y}/forecast".format(x=self.location_coords["x"],
                                                                                  y=self.location_coords["y"]))
        current_weather = r.json()['properties']['periods'][0]['detailedForecast']
        return 'Current weather in New Haven: ' + current_weather
