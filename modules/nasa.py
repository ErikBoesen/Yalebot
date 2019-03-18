from .base import Module
import os
import requests


class NASA(Module):
    DESCRIPTION = 'See the NASA image of the day'

    def response(self, query, message):
        # Get JSON data from NASA APOD API
        photo = requests.get('https://api.nasa.gov/planetary/apod?api_key=%s' % (os.environ.get('APOD_KEY') or 'DEMO_KEY')).json()

        # Send URL for image along with image's title
        return photo['url']
