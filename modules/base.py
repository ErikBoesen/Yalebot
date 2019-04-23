import os
import requests
from PIL import Image
from io import BytesIO


class Module:
    DESCRIPTION = ""
    ARGC = 0
    ACCESS_TOKEN = os.environ["GROUPME_ACCESS_TOKEN"]

    def __init__(self):
        print("Loaded module %s." % self.__class__.__name__)


class ImageUploader:
    MAX_IMAGE_WIDTH = 2000

    def upload_image(self, data) -> str:
        """
        Send image to GroupMe Image API.

        :param data: compressed image data.
        :return: URL of image now hosted on GroupMe server.
        """
        headers = {
            # TODO: we store this in every Module...
            "X-Access-Token": os.environ["GROUPME_ACCESS_TOKEN"],
            "Content-Type": "image/jpeg",
        }
        r = requests.post("https://image.groupme.com/pictures", data=data, headers=headers)
        return r.json()["payload"]["url"]

    def upload_pil_image(self, image: Image):
        output = BytesIO()
        image.save(output, format="JPEG")
        return self.upload_image(output.getvalue())

    def limit_image_size(self, image: Image):
        natural_width, natural_height = image.size
        if natural_width > self.MAX_IMAGE_WIDTH:
            width = self.MAX_IMAGE_WIDTH
            height = int(tear_width * tear_natural_height / tear_natural_width)
            image = image.resize((width, height), Image.ANTIALIAS)
        return image

    def get_portrait(self, user_id, group_id):
        # TODO: Figure out a way to not get entire list of members to find one
        members = requests.get(f"https://api.groupme.com/v3/groups/{group_id}?token={self.ACCESS_TOKEN}").json()["response"]["members"]
        for member in members:
            if member["user_id"] == user_id:
                return member["image_url"]

    def get_source_url(self, message):
        """
        Given complete image data, choose image to use from best source.
        First choose attached image, then use mentioned person's avatar, then sender's avatar.
        :return: URL of image to use.
        """
        image_attachments = [attachment for attachment in message["attachments"] if attachment["type"] == "image"]
        mention_attachments = [attachment for attachment in message["attachments"] if attachment["type"] == "mentions"]
        if len(image_attachments) > 0:
            # Get sent image
            return image_attachments[0]["url"]
        elif len(mention_attachments) > 0:
            return self.get_portrait(mention_attachments[0]["user_ids"][0], message["group_id"])
        else:
            # If no image was sent, use sender's avatar
            return message["avatar_url"]
