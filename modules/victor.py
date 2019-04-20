from .base import Module
import random


class Victor(Module):
    DESCRIPTION = "Affection for Monika"
    responses = []
    links = ["https://scontent-yyz1-1.cdninstagram.com/vp/56d445688c7774f8dc4e283558ebd7be/5D2FBE5B/t51.2885-15/e35/43075981_727705140917550_7862730829592735592_n.jpg?_nc_ht=scontent-yyz1-1.cdninstagram.com&se=8", "https://www.dailydot.com/wp-content/uploads/2018/10/loving_kermit.png", "https://i.pinimg.com/236x/74/58/f9/7458f981cc398b4feb3aaf3ac88ea171.jpg","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr981sN3a7xGvDO7eLNv5qao9doVPsX_yXt4RVEtcws1gOYdfR","https://data.whicdn.com/images/312331961/large.jpg"]

    def response(self, query, message):
        if len(self.responses) == 0:
            self.responses.extend(self.links)
            random.shuffle(self.responses)
        fullsend = self.responses.pop() + " @Monika"
        return fullsend
