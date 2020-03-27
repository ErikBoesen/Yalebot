from .base import ImageModule
from PIL import Image
import random


class Heaven(ImageModule):
    DESCRIPTION = "Memorialize the fallen"
    heaven = Image.open("resources/heaven.jpg")

    def response(self, query, message):
        source_url = self.get_source_url(message)
        portrait = self.pil_from_url(source_url)
        background = self.heaven.copy()

        portrait_natural_width, portrait_natural_height = portrait.size
        portrait_width = 600
        portrait_height = int(portrait_width * portrait_natural_height / portrait_natural_width)
        scaled_portrait = portrait.resize((portrait_width, portrait_height), Image.ANTIALIAS)

        background_width, background_height = background.size
        background.paste(scaled_portrait, ((background_width - portrait_width) // 2, 100))

        return "", self.upload_pil_image(background)
