from .base import Module


class Colleges(Module):
    DESCRIPTION = "Get links to groups for the various Yale residential colleges!"
    links = {
        "Yale University": "46649296/URP6KiXC",
        "University of Michigan": "46781389/hZehS1",
        "UNC Chapel Hill": "47712261/2K9zx7",
        "University of Virginia": "47680748/aLDXS1",
        "University of Miami": "48024399/XOwVQLZQ",
        "Baylor University": "42341652/O9zxGxij",
        "Virginia Tech": "46663109/rzmWS4",
        "University of Pennsylvania": "46633207/jo1Mk4wv",
        "Cornell University": "46579394/HJFvEV",
        "Liberty University": "49189743/Gjq3rDJX",
        "Columbia University": "46422965/fy1wXH",
    }
    links = {
        'Benjamin Franklin': '51337432/1P01Jawj',
        'Berkeley': '51337452/WS6dYrya',
        'Branford': '51337464/0DfxyBPh',
        'Davenport': '51337471/QydP3Uqp',
        'Ezra Stiles': '51337477/4SwHEUhM',
        'Grace Hopper': '51337487/NqXZODp7',
        'Jonathan Edwards': '51337498/t5Oq3QCc',
        'Morse': '51337503/ptRvZZoN',
        'Pauli Murray': '51337511/YNisIp1h',
        'Pierson': '51337516/umZfwuER',
        'Saybrook': '51337528/6wtXL5hD',
        'Silliman': '51337538/NuVpessh',
        'Timothy Dwight': '51337543/WU4U245f',
        'Trumbull': '51337553/VKFb0cmd',
    }

    def response(self, query, message):
        return '\n'.join(["%s -> https://groupme.com/join_group/%s" % (name, self.links[name]) for name in self.links])
