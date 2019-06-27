from .base import ImageModule
from PIL import Image


class Shield(ImageModule):
    DESCRIPTION = "Superimpose your residential college shield on a photo/"
    SIZE_RATIO = 4

    def __init__(self):
        super().__init__()

    def response(self, query, message):
        if query not in self.COLLEGES:
            return query + " is not recognized as a college name. Valid colleges: " + ", ".join(self.COLLEGES)
        source_url = self.get_source_url(message)
        background = self.pil_from_url(source_url)
        background_width, background_height = background.size
        smallest_dimension = min(background_width, background_height)
        # Crop to square
        left = (background_width - smallest_dimension) / 2
        top = (height - smallest_dimension) / 2
        right = background_width - left
        bottom = background_height - top
        background = background.crop((left, top, right, bottom))

        shield = Image.open("static/images/shields/" + query.lower().replace(" ", "") + ".png")
        shield_natural_width, shield_natural_height = background.size

        shield = self.resize(shield, background_width // self.SIZE_RATIO)
        processed_width, processed_height = shield.size
        background.paste(shield,
                         (int(background_width - processed_width - (processed_width // self.SIZE_RATIO)),
                          int(background_height - processed_height - (processed_width // self.SIZE_RATIO))),
                         shield)

        return "", self.upload_pil_image(background)
