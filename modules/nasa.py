from .base import Module
import os

class NASA(Module):
    DESCRIPTION = 'See beautiful space photos'
    def response(self, query, message):
         # Get JSON data from NASA APOD API
        photo = requests.get('https://api.nasa.gov/planetary/apod?api_key=%s' % (os.environ['APOD_KEY'] or 'DEMO_KEY')).json()

        # Send URL for image along with image's title
        reply(photo['url'])
