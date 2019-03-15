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

    font = ImageFont.truetype("resources/Lato-Regular.ttf", FONT_SIZE)
    small_font = ImageFont.truetype("resources/Lato-Regular.ttf", SMALL_FONT_SIZE)
    large_font = ImageFont.truetype("resources/Lato-Regular.ttf", LARGE_FONT_SIZE)

    def __init__(self):
        self.templates = {
            "drake": (self.mark_drake, 2),
            "yaledrake": (self.mark_drake, 2),
            "juice": ({
                "x": 327,
                "y": 145,
                "wrap": 20,
                "font": self.font,
                "font_size": self.FONT_SIZE,
                "color": self.BLACK,
                "center": True,
            }, {
                "x": 373,
                "y": 440,
                "wrap": 25,
                "font": self.small_font,
                "font_size": self.SMALL_FONT_SIZE,
                "color": self.BLACK,
                "center": True,
            }),
            "changemymind": ({
                "x": 579,
                "y": 460,
                "wrap": 19,
                "font": self.large_font,
                "font_size": self.LARGE_FONT_SIZE,
                "color": self.BLACK,
                "center": True,
            }),
            "catch": ({
                "x": 550,
                "y": 275,
                "wrap": 30,
                "font": self.font,
                "font_size": self.FONT_SIZE,
                "color": self.WHITE,
                "center": True,
            }, {
                "x": 250,
                "y": 90,
                "wrap": 20,
                "font": self.font,
                "font_size": self.FONT_SIZE,
                "color": self.WHITE,
                "center": True,
            }),
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
        """
        if (isinstance(mark_function, dict) and len(captions) < len(self.templates[template])) or len(captions) < captions_needed:
            return "Not enough captions provided (remember to separate with newlines)."
        """
        image = Image.open(f"resources/memes/{template}.jpg")
        draw = ImageDraw.Draw(image)
        self.mark_image(draw, captions, self.templates[template])
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

    def mark_image(self, draw: ImageDraw, captions, settings):
        for setting in settings:
            caption = captions.pop(0)
            lines = wrap(caption, setting.get("wrap"))
            for line_index, line in enumerate(lines):
                x = setting.get("x")
                y = setting.get("y")
                if setting.get("center"):
                    line_width, line_height = draw.textsize(line, font=setting.get("font"))
                    x -= line_width / 2
                    y -= line_width / 2
                draw.text((x, y + line_index * (setting.get("font_size") + 5)),
                          line,
                          font=setting.get("font") or self.font,
                          fill=setting.get("color") or self.BLACK)

    def mark_drake(self, draw: ImageDraw, captions):
        LEFT_BORDER = 350
        RIGHT_BORDER = 620

        START_Y = 100
        for caption_index, caption in enumerate(captions):
            lines = wrap(caption, 20)
            for line_index, line in enumerate(lines):
                draw.text((LEFT_BORDER, 80 * (caption_index + 1)**2 + self.FONT_SIZE * 1.3 * line_index), line, font=self.font, fill=self.BLACK)

    def mark_kirby(self, draw: ImageDraw, captions):
        BOARD_X, BOARD_Y = (80, 70)
        lines = wrap(captions[0], 20)
        for line_index, line in enumerate(lines):
            draw.text((BOARD_X, BOARD_Y + line_index * 25), line, font=self.small_font, fill=self.BLACK)
