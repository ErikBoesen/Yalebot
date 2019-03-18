from .base import Module, ImageUploader
from PIL import Image, ImageFont, ImageDraw
from textwrap import wrap
import requests
import os
import io


#class Meme:
class Meme(Module, ImageUploader):
    ARGC = 1

    FONT_SIZE = 30
    SMALL_FONT_SIZE = 20
    LARGE_FONT_SIZE = 50
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self):
        super().__init__()
        self.templates = {
            "drake": (
                {"position": (350, 100), "center": False},
                {"position": (350, 300), "center": False},
            ),
            "juice": (
                {"position": (327, 145)},
                {"position": (373, 440), "wrap": 25, "font_size": self.SMALL_FONT_SIZE},
            ),
            "changemymind": (
                {"position": (579, 420), "font_size": self.LARGE_FONT_SIZE},
            ),
            "catch": (
                {"position": (550, 275), "color": self.WHITE},
                {"position": (250, 90), "color": self.WHITE},
            ),
            "kirby": (
                {"position": (80, 70), "font_size": self.SMALL_FONT_SIZE, "center": False},
            ),
        }
        self.templates["yaledrake"] = self.templates["drake"]
        self.DESCRIPTION = "Generate memes! List the desired template, and then captions each on a new line. Supported templates: " + ", ".join(self.templates.keys())

    def response(self, query, message):
        captions = query.split("\n")

        template = captions.pop(0).strip().lower()
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

    def mark_image(self, draw: ImageDraw, captions, settings):
        for setting in settings:
            caption = captions.pop(0)
            lines = wrap(caption, setting.get("wrap", 20))
            for line_index, line in enumerate(lines):
                x, y = setting.get("position")
                font = ImageFont.truetype("resources/Lato-Regular.ttf", setting.get("font_size", self.FONT_SIZE))
                if setting.get("center", True):
                    line_width, line_height = draw.textsize(line, font=font)
                    x -= line_width / 2
                draw.text((x, y + line_index * (setting.get("font_size", self.FONT_SIZE) + 5)),
                          line,
                          font=font,
                          fill=setting.get("color", self.BLACK))
