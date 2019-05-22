import os
import requests
from PIL import Image
from io import BytesIO
import random


class Module:
    DESCRIPTION = ""
    ARGC = 0
    ARGUMENT_WARNING = "Not enough arguments!"
    ACCESS_TOKEN = os.environ.get("GROUPME_ACCESS_TOKEN")

    def __init__(self):
        print("Loaded module %s." % self.__class__.__name__)

    def wave(self):
        return "👋" + random.choice("🏻🏼🏽🏾🏿")

    def lines(self, query):
        return [line for line in query.split("\n") if line != ""]


class ImageModule(Module):
    def upload_image(self, data) -> str:
        """
        Send image to GroupMe Image API.

        :param data: compressed image data.
        :return: URL of image now hosted on GroupMe server.
        """
        headers = {
            "X-Access-Token": self.ACCESS_TOKEN,
            "Content-Type": "image/jpeg",
        }
        r = requests.post("https://image.groupme.com/pictures", data=data, headers=headers)
        return r.json()["payload"]["url"]

    def upload_pil_image(self, image: Image):
        output = BytesIO()
        image.save(output, format="JPEG", mode="RGB")
        return self.upload_image(output.getvalue())

    def pil_from_url(self, url):
        response = requests.get(url, stream=True)
        response.raw.decode_content = True
        return Image.open(response.raw)

    def resize(self, image: Image, width):
        natural_width, natural_height = image.size
        height = int(width * natural_height / natural_width)
        image = image.resize((width, height), Image.ANTIALIAS)
        return image

    def limit_image_size(self, image: Image, max_width=1000):
        natural_width, natural_height = image.size
        if natural_width > max_width:
            image = self.resize(image, max_width)
        return image

    def get_portrait(self, user_id, group_id):
        # TODO: Figure out a way to not get entire list of members to find one
        members = requests.get(f"https://api.groupme.com/v3/groups/{group_id}?token={self.ACCESS_TOKEN}").json()["response"]["members"]
        for member in members:
            if member["user_id"] == user_id:
                return member["image_url"]

    def get_source_url(self, message, include_avatar=True):
        """
        Given complete image data, extract the URL of the best image to use for a command.
        First choose attached image, then use mentioned person's avatar, then sender's avatar.
        :return: URL of image to use.
        """
        mention_attachments = [attachment for attachment in message.raw["attachments"] if attachment["type"] == "mentions"]
        if message.image_url is not None:
            # Get sent image
            return message.image_url
        elif len(mention_attachments) > 0:
            return self.get_portrait(mention_attachments[0]["user_ids"][0], message.group_id)
        # If no image was sent, use sender's avatar
        if include_avatar:
            return message.avatar_url
