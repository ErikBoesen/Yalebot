from .base import ImageModule
from PIL import Image
from io import BytesIO


class JPEG(ImageModule):
    DESCRIPTION = "Ever had an image that's too clear? Fix it"

    def response(self, query, message):
        source_url = self.get_source_url(message)
        image = self.pil_from_url(source_url)
        image = self.limit_image_size(image, width=400)
        output = BytesIO()
        image.save(output, format="JPEG", quality=2)
        return ("", self.upload_image(output.getvalue()))
