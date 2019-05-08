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
    YELLOW = (255, 255, 0)

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
            "jesus": (
                {"font_size": 12, "wrap": 13, "center": False},

                {"position": (68, 66)},
            ),
            "spiderman": (
                {"color": self.WHITE},

                {"position": (221, 121)},
                {"position": (617, 133)},
            ),
            "read": (
                {"color": self.WHITE, "center_vertical": True},

                {"position": (172, 189)},
                {"position": (322, 593)},
            ),
            "highfive": (
                {"center_vertical": True},

                {"position": (131, 89)},
                # {"position": (341, 23)},
                {"position": (133, 309)},
            ),
            "pyramid": (
                {"center": False, "center_vertical": True},

                {"position": (240, 150), "wrap": 30},
            ),
            "hannibal": (
                {"center_vertical": True, "color": self.WHITE, "font_size": self.LARGE_FONT_SIZE},

                {"position": (845, 420)},
                {"position": (300, 435)},
                {"position": (640, 1400), "wrap": 50, "color": self.YELLOW},
            ),
            "distractedboyfriend": (
                {},

                {"position": (360, 190)},
                {"position": (162, 257)},
                {"position": (490, 230), "wrap": 10},
            ),
            "woah": (
                {"center_vertical": True},

                {"position": (422, 285), "font_size": 100, "wrap": 10},
                {"position": (430, 864), "font_size": 50, "color": self.WHITE},
            ),
            "stencil": (
                {"center_vertical": True, "color": self.WHITE},

                {"position": (572, 346), "wrap": 10},
                {"position": (259, 405)},
                {"position": (368, 1043), "color": self.BLACK},
            ),
            "owl": (
                {"center_vertical": True},

                {"position": (169, 294), "color": self.WHITE},
                {"position": (654, 360)},
            ),
            "megan": (
                {"center_vertical": True, "color": self.YELLOW},

                {"position": (200, 240)},
            ),
            "dilemma": (
                {"center_vertical": True},

                {"position": (152, 136)},
                {"position": (353, 98)},
                {"position": (174, 810), "color": self.WHITE},
            ),
            "scroll": (
                {"center_vertical": True},

                {"position": (227, 634), "wrap": 15},
            ),
            "warm": (
                {"center_vertical": True, "font_size": self.LARGE_FONT_SIZE},

                {"position": (139, 618), "wrap": 10},
            ),
            "worldburn": (
                {"center_vertical": True, "color": self.WHITE},

                {"position": (365, 378)},
                {"position": (1000, 422)},
            ),
        }
        self.templates["yaledrake"] = self.templates["drake"]
        self.DESCRIPTION = "Generate memes! List the desired template, and then captions each on a new line. " + self.list_templates()

    def response(self, query, message):
        captions = query.split("\n")

        template_name = captions.pop(0).strip().lower()
        if self.templates.get(template_name) is None:
            return f"No template found called {template_name}. " + self.list_templates()
        captions_required = len(self.templates[template_name]) - 1
        if len(captions) < captions_required:
            return f"Not enough captions provided; {captions_required} required for template {template_name}. Remember to separate with newlines."
        image = Image.open(f"resources/memes/{template_name}.jpg")
        canvas = ImageDraw.Draw(image)
        self.draw_captions(canvas, captions, self.templates[template_name])

        return "", self.upload_pil_image(image)

    def draw_captions(self, canvas: ImageDraw, captions, settings):
        for setting in settings[1:]:
            caption = captions.pop(0)
            lines = wrap(caption, setting.get("wrap", settings[0].get("wrap", 20)))
            real_line_height = setting.get("font_size", settings[0].get("font_size", self.FONT_SIZE)) + 5
            lines_count = len(lines)
            for line_index, line in enumerate(lines):
                x, y = setting.get("position")
                font = ImageFont.truetype("resources/Lato-Regular.ttf", setting.get("font_size", settings[0].get("font_size", self.FONT_SIZE)))
                line_width, line_height = canvas.textsize(line, font=font)
                if setting.get("center", settings[0].get("center", True)):
                    x -= line_width / 2
                if setting.get("center_vertical", settings[0].get("center_vertical", False)):
                    y -= (lines_count * real_line_height) / 2
                canvas.text((x, y + line_index * real_line_height),
                            line,
                            font=font,
                            fill=setting.get("color", settings[0].get("color", self.BLACK)))
