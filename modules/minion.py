from .base import Module

BODY = """
⁣   😶😶😶😶😶  
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
    def response(self, query, message):
        return BODY % query.strip()
