from .base import ImageModule
from PIL import Image, ImageDraw


class Damn(ImageModule):
    DESCRIPTION = "Mimic Kendrick's iconic album cover"
    ARGC = 1

    def response(self, query, message):
        source_url = self.get_source_url(message, include_avatar=False)
        if source_url is None:
            background = Image.open("resources/damn.jpg")
        else:
            background = self.pil_from_url(source_url)
