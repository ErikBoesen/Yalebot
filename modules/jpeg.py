from .base import ImageModule
from PIL import Image
from io import BytesIO
import random


class JPEG(ImageModule):
    DESCRIPTION = "Ever had an image that's too clear? Fix it"

    def response(self, query, message):
        source_url = self.get_source_url(message)
        image = self.pil_from_url(source_url)
        image = self.limit_image_size(image, max_width=400)
        image = self.resize(image, width=random.randint(420, 1000))
        image = image.convert("RGB")
        output = BytesIO()
        image.save(output, format="JPEG", quality=2)
        return ("", self.upload_image(output.getvalue()))
