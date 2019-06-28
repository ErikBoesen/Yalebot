from .base import Module


class Groups(Module):
    DESCRIPTION = "Get links to various Yale GroupMe groups"
    links = {
        "Yale 2023": "46649296/xohKhqXv",
        "Yale Prom": "47397377/6SQ6Z9",
        "Robotics Yalies": "48299309/LfsRP2eP",
        "Directed Studies": "49954511/RJGSTgEU",
        "STEM": "50588247/5j7Ne6u8",
        "Black Yale 2023": "49447961/dUZwOQEp",
        "Korean Students": "50571775/dZYpXhb8",
        "First Generation students": "49418581/byuFtN4q",
        "LGBT+": "49376932/0wl2GN9F",
        "FSY": "50473402/gMWpQ8WK",
        "FOCUS": "50535013/HphGXnXD",
        "Cultural Connections": "50539019/Zi6masBV",
        "OIS": "51221005/yK4OvtHh",
        "First Gen": "49418581/byuFtN4q",

        "New York City": "46816234/B3PBXk",
        "DMV": "46655481/kpn04v",
        "New Jersey": "46963295/tmRi3T",
    }

    def response(self, query, message):
        return "\n".join(["%s -> https://groupme.com/join_group/%s" % (name, self.links[name]) for name in self.links])
