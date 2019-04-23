from .base import Module, ImageUploader
from PIL import Image, ImageFont, ImageDraw
from textwrap import wrap
import requests
import os


class Meme(Module, ImageUploader):
    ARGC = 1

    FONT_SIZE = 30
    SMALL_FONT_SIZE = 20
    LARGE_FONT_SIZE = 50
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def list_templates(self):
        return "Supported templates: " + ", ".join(self.templates.keys())

    def __init__(self):
        super().__init__()
        self.templates = {
            "drake": (
                {"center": False, "center_vertical": True},

                {"position": (350, 120)},
                {"position": (350, 405)},
            ),
            "juice": (
                {},

                {"position": (327, 145)},
                {"position": (373, 440), "wrap": 25, "font_size": self.SMALL_FONT_SIZE},
            ),
            "changemymind": (
                {"font_size": self.LARGE_FONT_SIZE},

                {"position": (579, 420)},
            ),
            "catch": (
                {"color": self.WHITE},

                {"position": (250, 90)},
                {"position": (550, 275)},
            ),
            "kirby": (
                {"font_size": self.SMALL_FONT_SIZE, "center": False},

                {"position": (80, 70)},
            ),
            "pocket": (
                {"wrap": 22, "font_size": self.SMALL_FONT_SIZE, "center": False},

                {"position": (570, 80)},
            ),
            "brain": (
                {"wrap": 17, "font_size": self.LARGE_FONT_SIZE, "center": False, "center_vertical": True},

                {"position": (10, 146)},
                {"position": (10, 450)},
                {"position": (10, 745)},
                {"position": (10, 1040)},
            ),
            "ask": (
                {"font_size": self.LARGE_FONT_SIZE, "center_vertical": True},

                {"position": (405, 450)},
            ),
            "whip": (
                {"color": self.WHITE, "center_vertical": True},

                {"position": (406, 438)},
                {"position": (160, 620)},
            ),
            "nut": (
                {"color": self.WHITE, "center_vertical": True},

                {"position": (405, 197)},
                {"position": (156, 280)},
            ),
            "handshake": (
                {"color": self.WHITE, "center_vertical": True},

                {"position": (332, 110)},
                {"position": (170, 390)},
                {"position": (648, 307)},
            ),
            "oil": (
                {"center_vertical": True},

                {"position": (200, 318)},
                {"position": (292, 695)},
            ),
            "letmein": (
                {"color": self.WHITE, "center_vertical": True},

                {"position": (128, 60)},
                {"position": (261, 177)},
            ),
            "sleep": (
                {"wrap": 18, "center_vertical": True},

                {"position": (134, 123)},
                {"position": (134, 367)},
            ),
            "zuck": (
                {"wrap": 26, "center_vertical": True},

                {"position": (544, 162)},
                {"position": (544, 486)},
            ),
            "load": (
                {"wrap": 18, "center_vertical": True},

                {"position": (128, 128)},
            ),
            "pooh": (
                {"center_vertical": True},

                {"position": (563, 141)},
                {"position": (563, 441)},
            ),
            "spectrum": (
                {"center_vertical": True},

                {"position": (115, 95)},
                {"position": (265, 95)},
                {"position": (115, 245)},
                {"position": (265, 245)},
            ),
            "hug": (
                {"font_size": self.LARGE_FONT_SIZE, "color": self.WHITE, "center": False},

                {"position": (15, 508)},
                {"position": (686, 301)},
                {"position": (601, 202), "wrap": 10, "center": True},
            ),
        }
        self.templates["yaledrake"] = self.templates["drake"]
        self.DESCRIPTION = "Generate memes! List the desired template, and then captions each on a new line. " + self.list_templates()

    def response(self, query, message):
        captions = query.split("\n")

        template = captions.pop(0).strip().lower()
        if self.templates.get(template) is None:
            return f"No template found called {template}. " + self.list_templates()
        if len(captions) < len(self.templates[template]) - 1:
            return "Not enough captions provided (remember to separate with newlines)."
        image = Image.open(f"resources/memes/{template}.jpg")
        draw = ImageDraw.Draw(image)
        self.mark_image(draw, captions, self.templates[template])

        image_url = self.upload_pil_image(image)
        return ("", image_url)

    def mark_image(self, draw: ImageDraw, captions, settings):
        for setting in settings[1:]:
            caption = captions.pop(0)
            lines = wrap(caption, setting.get("wrap", settings[0].get("wrap", 20)))
            real_line_height = setting.get("font_size", settings[0].get("font_size", self.FONT_SIZE)) + 5
            lines_count = len(lines)
            for line_index, line in enumerate(lines):
                x, y = setting.get("position")
                font = ImageFont.truetype("resources/Lato-Regular.ttf", setting.get("font_size", settings[0].get("font_size", self.FONT_SIZE)))
                line_width, line_height = draw.textsize(line, font=font)
                if setting.get("center", settings[0].get("center", True)):
                    x -= line_width / 2
                if setting.get("center_vertical", settings[0].get("center_vertical", False)):
                    y -= (lines_count * real_line_height) / 2
                draw.text((x, y + line_index * real_line_height),
                          line,
                          font=font,
                          fill=setting.get("color", settings[0].get("color", self.BLACK)))
