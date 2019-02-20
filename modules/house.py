from .base import Module

HOUSE = """
┏┓
┃┃╱╲ in
┃╱╱╲╲ this
╱╱╭╮╲╲house
▔▏┗┛▕▔ we
╱▔▔▔▔▔▔▔▔▔▔╲
%s
╱╱┏┳┓╭╮┏┳┓ ╲╲
▔▏┗┻┛┃┃┗┻┛▕▔
"""

class House(Module):
    def response(self, query, message):
        return HOUSE % query
