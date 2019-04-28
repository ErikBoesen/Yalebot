from .base import Module


class Groups(Module):
    DESCRIPTION = "Get links to various Yale GroupMe groups"
    links = {
        "Yale 2023": "46649296/URP6KiXC",
        "Yale Prom": "47397377/6SQ6Z9",
        "Robotics Yalies": "48299309/LfsRP2eP",
        "Directed Studies": "49954511/RJGSTgEU",
        "Black Yale 2023": "49447961/dUZwOQEp",

        "DMV Region": "46655481/kpn04v",
    }

    def response(self, query, message):
        return '\n'.join(["%s -> https://groupme.com/join_group/%s" % (name, self.links[name]) for name in self.links])
