from .base import Module
import requests
import os

class Weather(Module):
    NH_COORDINATES = {
        "x": 41.3083,
        "y": -72.9279
    }

    def response(self, query):
        r = requests.get("https://api.weather.gov/points/{x},{y}/forecast".format(x=self.NH_COORDINATES["x"],
                                                                                  y=self.NH_COORDINATES["y"]))
        forecast = r.json()['properties']['periods'][0]['detailedForecast']
        return 'Current weather in New Haven: ' + forecast
