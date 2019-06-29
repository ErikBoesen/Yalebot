from enum import Enum
import discord
from termcolor import colored
from datetime import datetime


class SenderType(Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"


class Message:
    def __init__(self, raw={}, text=None):
        self.raw = raw or {"attachments": []}
        self.text = text or raw.get("text")
        self.user_id = raw.get("user_id")
        time = raw.get("created_at", datetime.now())
        if type(time) == int:
            self.time = datetime.fromtimestamp(time)
        else:
            self.time = time
        self.name = raw.get("name", "Test")
        self.sender_type = SenderType(raw.get("sender_type", "user"))
        self.group_id = raw.get("group_id", "49940116")
        self.avatar_url = raw.get("avatar_url", "https://i.groupme.com/900x620.jpeg.bdc7a3233afc4832a3bce3fae95c2d8b.preview")
        print(self)

    def __repr__(self):
        return "{location} | {name}: {text}".format(location=self.group_id,
                                                    name=self.name,
                                                    text=self.text)

    @property
    def image_url(self):
        image_attachments = [attachment for attachment in self.raw["attachments"] if attachment["type"] == "image"]
        if image_attachments:
            return image_attachments[0]["url"]
