from .base import Module
from PIL import Image, ImageFont, ImageDraw
from textwrap import wrap
import requests
import os
import io


#class Meme:
class Meme(Module):
    ARGC = 1

    FONT_SIZE = 30
    SMALL_FONT_SIZE = 20
    LARGE_FONT_SIZE = 50
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    font = ImageFont.truetype("resources/Lato-Regular.ttf", self.FONT_SIZE)
    small_font = ImageFont.truetype("resources/Lato-Regular.ttf", self.SMALL_FONT_SIZE)
    large_font = ImageFont.truetype("resources/Lato-Regular.ttf", self.LARGE_FONT_SIZE)

    def __init__(self):
        self.templates = {
            "drake": (self.mark_drake, 2),
            "yaledrake": (self.mark_drake, 2),
            "juice": (self.mark_juice, 2),
            "changemymind": (self.mark_changemymind, 1),
            "catch": (self.mark_catch, 2),
            "kirby": (self.mark_kirby, 1),
        }
        self.DESCRIPTION = "Generate memes! List the desired template, and then captions each on a new line. Supported templates: " + ", ".join(self.templates.keys())
        super().__init__()

    def response(self, query, message):
        captions = query.split("\n")

        template = captions.pop(0).strip()
        if self.templates.get(template) is None:
            return f"No template found called {template}."
        mark_function, captions_needed = self.templates[template]
        if len(captions) < captions_needed:
            return "Not enough captions provided (remember to separate with newlines)."
        image = Image.open(f"resources/memes/{template}.jpg")
        draw = ImageDraw.Draw(image)
        mark_function(draw, captions)
        """
        image.show()
        return
        """
        output = io.BytesIO()
        image.save(output, format="JPEG")
        image_url = self.upload_image(output.getvalue())
        return ("", image_url)

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

    def mark_drake(self, draw: ImageDraw, captions):
        LEFT_BORDER = 350
        RIGHT_BORDER = 620

        START_Y = 100
        for caption_index, caption in enumerate(captions):
            lines = wrap(caption, 20)
            for line_index, line in enumerate(lines):
                draw.text((LEFT_BORDER, 80 * (caption_index + 1)**2 + self.FONT_SIZE * 1.3 * line_index), line, font=self.font, fill=self.BLACK)

    def mark_juice(self, draw: ImageDraw, captions):
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

    def mark_changemymind(self, draw: ImageDraw, captions):
        SIGN_X, SIGN_Y = (579, 460)
        lines = wrap(captions[0], 19)
        for line_index, line in enumerate(lines):
            line_width, line_height = draw.textsize(line, font=self.large_font)
            draw.text((SIGN_X-line_width/2, SIGN_Y-line_height/2 + line_index * 55), line, font=self.large_font, fill=self.BLACK)

    def mark_catch(self, draw: ImageDraw, captions):

        ARMS_X, ARMS_Y = (550, 275)
        lines = wrap(captions[0])
        for line_index, line in enumerate(lines):
            line_width, line_height = draw.textsize(line, font=self.font)
            draw.text((ARMS_X-line_width/2, ARMS_Y-line_height/2 + line_index * 35), line, font=self.font, fill=self.WHITE)

        BALL_X, BALL_Y = (250, 90)
        lines = wrap(captions[1], 20)
        for line_index, line in enumerate(lines):
            line_width, line_height = draw.textsize(line, font=self.font)
            draw.text((BALL_X-line_width/2, BALL_Y-line_height/2 + line_index * 35), line, font=self.font, fill=self.WHITE)

    def mark_kirby(self, draw: ImageDraw, captions):
        BOARD_X, BOARD_Y = (80, 70)
        lines = wrap(captions[0], 20)
        for line_index, line in enumerate(lines):
            draw.text((BOARD_X, BOARD_Y + line_index * 25), line, font=self.small_font, fill=self.BLACK)
