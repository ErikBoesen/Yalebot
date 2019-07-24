import os
import requests
from PIL import Image, ExifTags
from io import BytesIO
import random


class Module:
    DESCRIPTION = ""
    ARGC = 0
    ARGUMENT_WARNING = "Not enough arguments!"
    ACCESS_TOKEN = os.environ.get("GROUPME_ACCESS_TOKEN")

    COLLEGES = {
        "Benjamin Franklin",
        "Berkeley",
        "Branford",
        "Davenport",
        "Ezra Stiles",
        "Grace Hopper",
        "Jonathan Edwards",
        "Morse",
        "Pauli Murray",
        "Pierson",
        "Saybrook",
        "Silliman",
        "Timothy Dwight",
        "Trumbull",
    }

    def __init__(self):
        print("Loaded module %s." % self.__class__.__name__)

    def wave(self):
        """
        Generate a wave emoji with a random skin color.
        """
        return "👋" + random.choice("🏻🏼🏽🏾🏿")

    def lines(self, query):
        """
        Split input into each individual line, for multiple-argument commands.
        """
        return [line for line in query.split("\n") if line != ""]

    def bullet_list(self, pairs, embellish_first=False) -> str:
        """
        Generate nicely-formatted list of data points about some object.
        :param pairs: list of tuples, each having a key and a value.
        """
        response = ""
        if embellish_first:
            if type(pairs) == tuple:
                pairs = list(pairs)
            title, value = pairs.pop(0)
            response += f"--- {title}: {value} ---\n"
        for title, value in pairs:
            if value:
                response += f"{title}: {value}\n"
        return response

    @staticmethod
    def safe_spaces(text):
        """
        BUILD A HOME HERE.
        Replace spaces with Unicode character "Three-Per-Em Space" which GroupMe won't combine on mobile.
        Useful for sending ASCII art.

        :param text: text in which to replace spaces.
        :return: text that's safe to send.
        """
        text.replace("\t", " " * 4)
        return text.replace(" ", "\u2004")

    def normalize(self, text):
        """
        Get everything into an easily comparable format.
        :param text: input text.
        :return: lowercase text without spaces or other confounding content.
        """
        return text.lower().replace(" ", "")


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

    def rotate_upright(self, image: Image):
        """
        Rotate a PIL image to upright depending on its current orientation according to EXIF data.
        """
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        return image

    def upload_pil_image(self, image: Image):
        """
        Given a PIL image, convert it into a format that can be uploaded to GroupMe's image API, then do that.
        """
        output = BytesIO()
        image.save(output, format="JPEG", mode="RGB")
        return self.upload_image(output.getvalue())

    def pil_from_url(self, url):
        """
        Download and process an image from a given URL for later manipulation.
        :param url: URL of image to download.
        :return: PIL image for later manipulation.
        """
        response = requests.get(url, stream=True)
        response.raw.decode_content = True
        image = Image.open(response.raw)
        # Rotation must be performed now as conversion to RGB drops EXIF data
        image = self.rotate_upright(image)
        image = image.convert("RGB")
        return image

    def resize(self, image: Image, width):
        """
        Resize a PIL image down to a some maximum width.
        Useful for limiting image size.
        :param image: PIL image to resize.
        :param width: maximum width.
        :return: resized image.
        """
        natural_width, natural_height = image.size
        height = int(width * natural_height / natural_width)
        image = image.resize((width, height), Image.ANTIALIAS)
        return image

    def limit_image_size(self, image: Image, max_width=1000):
        """
        Limit an image's size in its largest dimension.
        Will do nothing if image is already small enough.
        :param image: PIL image to scale.
        :param max_width: largest size to allow image to be.
        :return: resized image.
        """
        natural_width, natural_height = image.size
        if natural_width > max_width:
            image = self.resize(image, max_width)
        return image

    def get_portrait(self, user_id, group_id):
        """
        Get a given user's portrait in a given group.
        :param user_id: ID of user.
        :param group_id: ID of group that they use the portrait in.
        :reutrn: URL of their portrait.
        """
        # TODO: Figure out a way to not get entire list of members to find one
        members = requests.get(f"https://api.groupme.com/v3/groups/{group_id}?token={self.ACCESS_TOKEN}").json()["response"]["members"]
        for member in members:
            if member["user_id"] == user_id:
                return member["image_url"]

    def get_source_url(self, message, include_avatar=True):
        """
        Given complete image data, extract the URL of the best image to use for a command.
        First choose attached image, then use mentioned person's avatar, then sender's avatar.
        :param message: data of message to extract URL from.
        :param include_avatar: should we use the avatar? Sometimes this may be undesired if another default is desired.
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
