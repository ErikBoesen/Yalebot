from .base import Module
import random

class Sad(Module):
    PICTURES = [
        'https://vetstreet.brightspotcdn.com/dims4/default/3407f3b/2147483647/thumbnail/645x380/quality/90/?url=https%3A%2F%2Fvetstreet-brightspot.s3.amazonaws.com%2Ffb%2F31%2F032a6aae436a9821acda211044fb%2Fbulldog-ap-rn4myi-645.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/1/13/Clyde_The_Bulldog.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/1/14/Female_English_Bulldog.png',
        'https://upload.wikimedia.org/wikipedia/commons/5/5c/English_Bulldog_puppy.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/d/db/English_Bulldog_about_to_sleep.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/e/e5/Axel%2C_the_English_Bulldog.jpg',
        'https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/06014411/bulldog-puppy-asleep-on-couch.jpg',
    ]
    def response(self, query):
        return random.choice(self.PICTURES)
