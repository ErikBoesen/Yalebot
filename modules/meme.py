from .base import Module
from PIL import Image, ImageFont, ImageDraw
from textwrap import wrap
import requests
import os
import io


class Meme(Module):
    FONT_SIZE = 30
    SMALL_FONT_SIZE = 15
    BLACK = (0, 0, 0)
    TEMPLATE_NAME = ""
    def __init__(self):
        self.template = Image.open("resources/memes/%s.jpg" % self.TEMPLATE_NAME)
        self.font = ImageFont.truetype("resources/Lato-Regular.ttf", self.FONT_SIZE)
        self.small_font = ImageFont.truetype("resources/Lato-Regular.ttf", self.SMALL_FONT_SIZE)
        super().__init__()

    def response(self, query):
        image = self.template.copy()
        captions = query.split("\n")
        draw = ImageDraw.Draw(image)

        self.mark_image(draw, captions)
        output = io.BytesIO()
        image.save(output, format="JPEG")
        image_url = self.upload_image(output.getvalue())
        print(image_url)
        return image_url

    def mark_image(self, draw: ImageDraw, captions):
        """
        Should be overwritten in subclass.
        """
        raise NotImplementedError

    def upload_image(self, data) -> str:
        """
        Send image to GroupMe Image API.

        :param data: compressed image data.
        :return: URL of image now hosted on GroupMe server.
        """
        headers = {
            "X-Access-Token": os.environ["GROUPME_ACCESS_TOKEN"],
            "Content-Type": "image/jpeg",
        }
        r = requests.post("https://image.groupme.com/pictures", data=data, headers=headers)
        return r.json()["payload"]["url"]

class Drake(Meme):
    TEMPLATE_NAME = "drake"
    def mark_image(self, draw: ImageDraw, captions):
        LEFT_BORDER = 350
        RIGHT_BORDER = 620

        START_Y = 100
        for caption_index, caption in enumerate(captions):
            lines = wrap(caption, 20)
            for line_index, line in enumerate(lines):
                draw.text((LEFT_BORDER, 80 * (caption_index + 1)**2 + self.FONT_SIZE * 1.3 * line_index), line, font=self.font, fill=self.BLACK)

class YaleDrake(Drake):
    TEMPLATE_NAME = "yaledrake"

class Juice(Meme):
    TEMPLATE_NAME = "juice"
    def mark_image(self, draw: ImageDraw, captions):
        HEAD_X, HEAD_Y = (327, 145)
        JUG_X, JUG_Y = (373, 440)

        lines = wrap(captions[0], 20)
        for line_index, line in enumerate(lines):
            line_width, line_height = draw.textsize(line, font=self.font)
            draw.text((HEAD_X-line_width/2, HEAD_Y-line_height/2 + line_index * 35), line, font=self.font, fill=self.BLACK)
        lines = wrap(captions[1], 25)
        for line_index, line in enumerate(lines):
            line_width, line_height = draw.textsize(line, font=self.small_font)
            draw.text((JUG_X-line_width/2, JUG_Y-line_height/2 + line_index * 20), line, font=self.small_font, fill=self.BLACK)
