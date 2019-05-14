from .base import ImageModule
from PIL import Image


class JPEG(ImageModule):
    DESCRIPTION = "Ever had an image that's too clear? Fix it"

    def response(self, query, message):
        source_url = self.get_source_url(message)
        image = self.pil_from_url(source_url)
        return ("", self.upload_pil_image(image, quality=20))
