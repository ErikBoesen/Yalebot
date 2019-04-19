from .base import Module, ImageUploader
from PIL import Image, ImageDraw
import random
from io import BytesIO
# TODO: This is so complicated for literally just reading an image from a URL
from skimage import io


class Crist(Module, ImageUploader):
    DESCRIPTION = "Memorialize the fallen"
    heaven = Image.open("resources/heaven.jpg")

    def response(self, query, message):
        source_url = self.get_source_url(message)
        image = io.imread(source_url)[:, :, :3]
        portrait = Image.fromarray(image)
        background = self.heaven.copy()

        portrait_natural_width, portrait_natural_height = portrait.size
        portrait_width = 600
        portrait_height = int(portrait_width * portrait_natural_height / portrait_natural_width)
        scaled_portrait = portrait.resize((portrait_width, portrait_height), Image.ANTIALIAS)
        processed_width, processed_height = processed_heart.size

        background_width, background_height = background.size
        background.paste(scaled_portrait, ((background_width - portrait_width) / 2, 100), scaled_portrait)

        output = BytesIO()
        background.save(output, format="JPEG")
        return "", self.upload_image(output.getvalue())
