from .base import Module


class Groups(Module):
    DESCRIPTION = "Get links to various Yale GroupMe groups"
    links = {
    }

    def response(self, query, message):
        return "\n".join(["%s -> https://groupme.com/join_group/%s" % (name, self.links[name]) for name in self.links])
