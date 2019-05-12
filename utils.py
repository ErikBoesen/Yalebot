from enum import Enum
import discord
from termcolor import colored


class Platform(Enum):
    GROUPME = 0
    DISCORD = 1
    FACEBOOK = 2


class SenderType(Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"


class Message:
    def __init__(self, raw, text, platform=None, user_id=None, name=None, sender_type=SenderType.USER, group_id=None, avatar_url=None):
        self.raw = raw
        self.text = text
        self.user_id = user_id
        self.name = name
        self.sender_type = sender_type
        self.group_id = group_id
        self.avatar_url = avatar_url

    @classmethod
    def from_groupme(cls, message: dict):
        return cls(message,
                   text=message.get("text"),
                   platform=Platform.GROUPME,
                   user_id=message.get("user_id"),
                   name=message.get("name"),
                   sender_type=message.get("sender_type"),
                   group_id=message.get("group_id"),
                   avatar_url=message.get("avatar_url"))

    @classmethod
    def from_discord(cls, message: discord.message):
        return cls(message,
                   text=message.content,
                   platform=Platform.DISCORD,
                   user_id=message.id,
                   name=message.author.display_name,
                   avatar_url=message.author.avatar_url)

    @classmethod
    def from_facebook(cls, message: dict):
        return cls(message,
                   text=message["message"]["text"],
                   platform=Platform.FACEBOOK,
                   user_id=message["sender"]["id"],
                   name=None)
