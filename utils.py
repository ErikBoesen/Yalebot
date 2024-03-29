from enum import Enum
from termcolor import colored
from datetime import datetime


class SenderType(Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"


class Message:
    def __init__(self, raw={}, text=None):
        """
        Translate raw message data into an easily usable format.
        :param raw: a dictionary of raw message data.
        :param text: raw text of message, useful for saving verbosity when testing.
        """
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
        self.group_id = raw.get("group_id")
        self.bot_id = raw.get("bot_id")
        self.token = raw.get("token")
        self.avatar_url = raw.get("avatar_url", "https://i.groupme.com/1280x960.jpeg.8f50fab1751b461abcb5d510d7fe4b83")
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
