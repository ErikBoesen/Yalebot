from .base import ImageModule
from PIL import Image
from io import BytesIO


class JPEG(ImageModule):
    DESCRIPTION = "Ever had an image that's too clear? Fix it"

    def response(self, query, message):
        source_url = self.get_source_url(message)
        image = self.pil_from_url(source_url)
        output = BytesIO()
        image.save(output, format="JPEG", quality=1)
        return self.upload_image(output.getvalue())
