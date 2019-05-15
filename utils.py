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
        if time is None:
            self.time = datetime.now()
        elif type(time) == int:
            self.time = datetime.fromtimestamp(time)
        else:
            self.time = time
        self.name = name
        self.sender_type = sender_type
        self.group_id = group_id
        self.avatar_url = avatar_url
        print(self)

    def __repr__(self):
        color = {Platform.GROUPME: "green", Platform.DISCORD: "magenta", Platform.FACEBOOK: "blue"}.get(self.platform)
        return colored("{location} | {name}: {text}".format(location=self.get_location(),
                                                            name=self.name,
                                                            text=self.text), color)

    def get_location(self):
        if self.platform == Platform.GROUPME:
            return self.group_id
        if self.platform == Platform.DISCORD:
            return "#" + self.raw.channel.name
        if self.platform == Platform.FACEBOOK:
            # TODO
            pass

    @classmethod
    def from_groupme(cls, message: dict):
        return cls(message,
                   text=message.get("text"),
                   platform=Platform.GROUPME,
                   user_id=message.get("user_id"),
                   time=message.get("created_at"),
                   name=message.get("name"),
                   sender_type=SenderType(message.get("sender_type")),
                   group_id=message.get("group_id"),
                   avatar_url=message.get("avatar_url"))

    @classmethod
    def from_discord(cls, message: discord.message):
        return cls(message,
                   text=message.content,
                   platform=Platform.DISCORD,
                   user_id=message.id,
                   time=message.created_at,
                   name=message.author.display_name,
                   avatar_url=message.author.avatar_url)

    @classmethod
    def from_facebook(cls, message: dict):
        return cls(message,
                   text=message["message"]["text"],
                   platform=Platform.FACEBOOK,
                   user_id=message["sender"]["id"],
                   time=message["timestamp"] // 1000,
                   name="Friend")

    @property
    def image_url(self):
        if self.platform == Platform.GROUPME:
            image_attachments = [attachment for attachment in self.raw["attachments"] if attachment["type"] == "image"]
            if image_attachments:
                return image_attachments[0]["url"]
