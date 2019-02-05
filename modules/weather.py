from .base import Module
import requests
import os

class Weather(Module):
    location_name = "New Haven, CT"
    location_coords = {
        "x": 41.3083,
        "y": -72.9279
    }
    request_params = {
        "token": os.environ["WEATHER_KEY"]
    }
    def response(self, query):
        weather_response = requests.get('https://api.weather.gov/points/' + location_coords['x'] + ',' + location_coords['y'] + '/forecast').json()
        current_weather = weather_response['properties']['periods'][0]['detailedForecast']
        return current_weather
