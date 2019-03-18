from .base import Module
from textwrap import wrap

HOUSE = """┏┓
┃┃╱╲ in
┃╱╱╲╲ this
╱╱╭╮╲╲house
▔▏┗┛▕▔ we
╱▔▔▔▔▔▔▔▔▔▔╲
%s
╱╱┏┳┓╭╮┏┳┓ ╲╲
▔▏┗┻┛┃┃┗┻┛▕▔"""


class House(Module):
    DESCRIPTION = "What do we do in this house?"
    ARGC = 1

    def response(self, query, message):
        return HOUSE % "\n".join(wrap(query, 30))
