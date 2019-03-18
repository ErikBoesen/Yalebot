from .base import Module
import random


class Sad(Module):
    DESCRIPTION = "Instantly dispel all mental health problems"
    PICTURES = [
        "https://vetstreet.brightspotcdn.com/dims4/default/3407f3b/2147483647/thumbnail/645x380/quality/90/?url=https%3A%2F%2Fvetstreet-brightspot.s3.amazonaws.com%2Ffb%2F31%2F032a6aae436a9821acda211044fb%2Fbulldog-ap-rn4myi-645.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/13/Clyde_The_Bulldog.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/14/Female_English_Bulldog.png",
        "https://upload.wikimedia.org/wikipedia/commons/5/5c/English_Bulldog_puppy.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/db/English_Bulldog_about_to_sleep.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/e/e5/Axel%2C_the_English_Bulldog.jpg",
        "https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/06014411/bulldog-puppy-asleep-on-couch.jpg",
        "https://static.boredpanda.com/blog/wp-content/uploads/2015/04/bulldog-puppy-cute-dog-photography-23__605.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIMZVUg9Y630THs3IxHQkxNJ_zjOYEqF3N0Dk8NNswsi-y9gFw",
        "https://naturaldogcompany.com/wp-content/uploads/2017/09/Cute-English-Bulldog-Puppies-web.jpg",
        "https://i.pinimg.com/originals/d5/99/4b/d5994ba1f2fd2af3fff905888cadbd32.jpg",
        "https://images.unsplash.com/photo-1519052537078-e6302a4968d4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80",  # cat
    ]

    def response(self, query, message):
        return random.choice(self.PICTURES)
