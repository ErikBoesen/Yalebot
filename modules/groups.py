from .base import Module


class Groups(Module):
    DESCRIPTION = "Get links to various Yale GroupMe groups"
    links = {
        "California": "58985981/AC4xwNR3",
        "Computer Science": "58985302/ZsAYNq7R",
        "LGBT": "57668130/3G1UEdSC",
        "Yale Asians": "58153915/NmNIq17c",
        "Yalecraft??": "57444490/iwNiIjzV",
        "Hot climate chat": "58986052/bkazz6KU",
        "Black Yalies": "58689269/tK9k6qlp",
        "Cold Climate Yale": "59030987/6STQvYTs",
        "Yalie Muslims": "59121570/uHTsEbj8",
        "Yalie MENA": "59420691/DS59UJUY",
    }

    def response(self, query, message):
        return "\n".join(["%s -> https://groupme.com/join_group/%s" % (name, self.links[name]) for name in self.links])
