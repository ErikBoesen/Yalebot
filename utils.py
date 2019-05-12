from enum import Enum
import discord


class Platform(Enum):
    GROUPME = 0
    DISCORD = 1
    FACEBOOK = 2


class SenderType(Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"


class Message:
    def __init__(self, raw, text, platform=None, user_id=None, name=None, sender_type=SenderType.USER):
        self.raw = raw
        self.text = text
        self.user_id = user_id
        self.name = name
        self.sender_type = sender_type

    @classmethod
    def from_groupme(cls, message: dict):
        return cls(message,
                   text=message["text"],
                   platform=Platform.GROUPME,
                   user_id=message["user_id"],
                   name=message["name"],
                   sender_type=message["sender_type"])

    @classmethod
    def from_discord(cls, message: discord.message):
        return cls(message,
                   text=message.content,
                   platform=Platform.DISCORD,
                   user_id=message.id,
                   name=None)

    @classmethod
    def from_facebook(cls, message: dict):
        return cls(message,
                   text=message["message"]["text"],
                   platform=Platform.FACEBOOK,
                   user_id=message["sender"]["id"],
                   name=None)
