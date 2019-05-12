from enum import Enum
import discord
from termcolor import colored
from datetime import datetime


class Platform(Enum):
    GROUPME = 0
    DISCORD = 1
    FACEBOOK = 2


class SenderType(Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"


class Message:
    def __init__(self, raw, text, platform=None, user_id=None, time=None, name=None, sender_type=SenderType.USER, group_id=None, avatar_url=None):
        self.raw = raw
        self.text = text
        self.platform = platform
        self.user_id = user_id
        if timestamp is None:
            self.time = datetime.now()
        elif type(timestamp) == int:
            self.time = datetime.from_timestamp(timestamp)
        else:
            self.time = time
        self.timestamp = timestam
        self.name = name
        self.sender_type = sender_type
        self.group_id = group_id
        self.avatar_url = avatar_url
        print(self)

    def __repr__(self):
        color = {Platform.GROUPME: "cyan", Platform.DISCORD: "magenta", Platform.FACEBOOK: "blue"}[self.platform]
        return colored("{time} | {location} | {name}: {text}".format(time=self.time.strftime("%y:%m:%d:%H:%M:%S"),
                                                                     location=self.get_location(),
                                                                     name=self.name,
                                                                     text=self.text), color)

    def get_location(self):
        if self.platform == Platform.GROUPME:
            return self.group_id
        if self.platform == Platform.DISCORD:
            return self.raw.channel.name
        if self.platform == Platform.FACEBOOK:
            # TODO
            pass

    @classmethod
    def from_groupme(cls, message: dict):
        return cls(message,
                   text=message.get("text"),
                   platform=Platform.GROUPME,
                   user_id=message.get("user_id"),
                   timestamp=message.get("created_at"),
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
                   timestamp=int(message.created_at),
                   name=message.author.display_name,
                   avatar_url=message.author.avatar_url)

    @classmethod
    def from_facebook(cls, message: dict):
        return cls(message,
                   text=message["message"]["text"],
                   platform=Platform.FACEBOOK,
                   user_id=message["sender"]["id"],
                   timestamp=message["timestamp"] // 1000,
                   name=None)
