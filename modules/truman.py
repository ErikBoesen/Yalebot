from .base import Module, ImageUploader
from PIL import Image
from io import BytesIO
from pytesseract import image_to_string
# TODO: This is so complicated for literally just reading an image from a URL
from skimage import io


class Truman(Module, ImageUploader):
    DESCRIPTION = "Is your battery sinfully low?"

    def response(self, query, message):
        source_url = self.get_source_url(message)

        image = io.imread(source_url)[:, :, :3]
        pil_image = Image.fromarray(image)
        image_to_string(pil_image)

        output = BytesIO()
        pil_image.save(output, format="JPEG")
        return "", self.upload_image(output.getvalue())
