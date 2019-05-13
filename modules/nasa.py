from .base import Module
import os
import requests


class NASA(Module):
    DESCRIPTION = "See the NASA image of the day"

    def response(self, query, message):
        # Get JSON data from NASA APOD API
        photo = requests.get("https://api.nasa.gov/planetary/apod?api_key=" + (os.environ.get("APOD_KEY") or "DEMO_KEY")).json()

        # Send URL for image along with image title
        return ["NASA Image of the Day " + photo["date"] + "\n\n" + photo["description"],
                photo["hdurl"]]
