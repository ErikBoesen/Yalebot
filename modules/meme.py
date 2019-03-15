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

    def __init__(self):
        self.templates = {
            "drake": ({
                "x": 350, "y": 100,
                "wrap": 20,
                "font_size": self.FONT_SIZE,
                center: False,
            }, {
                "x": 350, "y": 300,
                "wrap": 20,
                "font_size": self.FONT_SIZE,
                "center": False,
            },),
            "juice": ({
                "x": 327, "y": 145,
                "wrap": 20,
                "font_size": self.FONT_SIZE,
            }, {
                "x": 373, "y": 440,
                "wrap": 25,
                "font_size": self.SMALL_FONT_SIZE,
            },),
            "changemymind": ({
                "x": 579, "y": 460,
                "wrap": 19,
                "font_size": self.LARGE_FONT_SIZE,
            },),
            "catch": ({
                "x": 550, "y": 275,
                "wrap": 30,
                "font_size": self.FONT_SIZE,
                "color": self.WHITE,
            }, {
                "x": 250, "y": 90,
                "wrap": 20,
                "font_size": self.FONT_SIZE,
                "color": self.WHITE,
            },),
            "kirby": ({
                "x": 80, "y": 70,
                "wrap": 20,
                "font_size": self.SMALL_FONT_SIZE,
            },),
        }
        self.templates["yaledrake"] = self.templates["drake"]
        self.DESCRIPTION = "Generate memes! List the desired template, and then captions each on a new line. Supported templates: " + ", ".join(self.templates.keys())
        super().__init__()

    def response(self, query, message):
        captions = query.split("\n")

        template = captions.pop(0).strip()
        if self.templates.get(template) is None:
            return f"No template found called {template}."
        if len(captions) < len(self.templates[template]):
            return "Not enough captions provided (remember to separate with newlines)."
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
                if setting.get("center") or True:
                    line_width, line_height = draw.textsize(line, font=setting.get("font"))
                    x -= line_width / 2
                draw.text((x, y + line_index * (setting.get("font_size") + 5)),
                          line,
                          font=ImageFont.truetype("resources/Lato-Regular.ttf", setting.get("font_size")),
                          fill=setting.get("color") or self.BLACK)
