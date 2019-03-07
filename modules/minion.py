from .base import Module

BODY = """>⁣   😶😶😶😶😶  
  😶😶😶😶😶😶
 😶😶😶😶😶😶😶
😶😶😶💣💣😶😶😶
💣💣💣💿💿💣💣💣
💣💣💣💿💿💣💣💣
😶😶😶💣💣😶😶😶
😶😶😶😶😶😶😶😶
😶😶💣😶😶💣😶😶
😶😶⁣😶💣💣😶😶😶
👖😶😶😶😶😶😶👖
😶👖👖👖👖👖👖😶
😶👖👖👖👖👖👖😶
👖👖👖👖👖👖👖👖
👖👖👖👖👖👖👖👖
👖👖👖    👖👖👖
👖👖👖    👖👖👖
  %s        %s
"""

class Minion(Module):
    DESCRIPTION = "Die"
    ARGC = 1
    def response(self, query, message):
        emote = query.strip()
        return BODY % (emote, emote)
