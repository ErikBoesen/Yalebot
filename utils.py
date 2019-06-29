from enum import Enum
import discord
from termcolor import colored
from datetime import datetime


class SenderType(Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"


class Message:
    def __init__(self, raw, text, user_id=None, time=None, name=None, sender_type=SenderType.USER, group_id=None, avatar_url=None):
        self.raw = raw
        self.text = text
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
        return "{location} | {name}: {text}".format(location=self.group_id,
                                                    name=self.name,
                                                    text=self.text)

    @classmethod
    def from_groupme(cls, message: dict):
        return cls(message,
                   text=message.get("text"),
                   user_id=message.get("user_id"),
                   time=message.get("created_at"),
                   name=message.get("name"),
                   sender_type=SenderType(message.get("sender_type")),
                   group_id=message.get("group_id"),
                   avatar_url=message.get("avatar_url"))

    @property
    def image_url(self):
        image_attachments = [attachment for attachment in self.raw["attachments"] if attachment["type"] == "image"]
        if image_attachments:
            return image_attachments[0]["url"]
