from .base import Module
import random


class Wholesome(Module):
    DESCRIPTION = "Send random wholesome meme"
    responses = ["https://www.dailydot.com/wp-content/uploads/2018/10/loving_kermit.png", "https://i.pinimg.com/236x/74/58/f9/7458f981cc398b4feb3aaf3ac88ea171.jpg", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr981sN3a7xGvDO7eLNv5qao9doVPsX_yXt4RVEtcws1gOYdfR", "https://data.whicdn.com/images/312331961/large.jpg"]

    def response(self, query, message):
        return random.choice(self.responses)
