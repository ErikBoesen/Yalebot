from .base import Module


class Groups(Module):
    DESCRIPTION = "Get links to various Yale GroupMe groups"
    links = {
        "LGBT": "57444490/iwNiIjzV",
        "Also LGBT": "57668130/3G1UEdSC",
        "Yalecraft??": "57444490/iwNiIjzV",
    }

    def response(self, query, message):
        return "\n".join(["%s -> https://groupme.com/join_group/%s" % (name, self.links[name]) for name in self.links])
