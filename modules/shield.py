from .base import ImageModule
from PIL import Image, ImageDraw
import random


class Shield(ImageModule):
    DESCRIPTION = "Superimpose your residential college shield on a photo/"
    SIZE_RATIO = 6

    def __init__(self):
        super().__init__()
        shields = {name.lower(): Image.open("resources/shields/" + name.replace(" ", "") + ".png") for name in self.COLLEGES}

    def response(self, query, message):
        if query not in self.COLLEGES:
            return query + " is not recognized as a college name. Valid colleges: " + ", ".join(self.COLLEGES)
        background = self.pil_from_url(source_url)
        shield = self.shields[query.lower()].copy()
        shield_width, shield_height = background.size
        shield_width //= self.SIZE_RATIO
        shield_height //= self.SIZE_RATIO

        processed_heart = heart.resize((heart_size, heart_size), Image.ANTIALIAS)
        background.paste(processed_heart,
                         (int(random.random() * (image_width - processed_width)), int(random.random() * (image_height - processed_height))),
                         processed_heart)

        return "", self.upload_pil_image(background)
