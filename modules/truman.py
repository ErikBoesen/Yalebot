from .base import Module, ImageUploader
from PIL import Image
from io import BytesIO
import re
from pytesseract import image_to_string
# TODO: This is so complicated for literally just reading an image from a URL
from skimage import io


class Truman(Module, ImageUploader):
    DESCRIPTION = "Is your battery sinfully low?"
    PERCENTAGE_RE = re.compile(r"(\d+)%")

    def response(self, query, message):
        source_url = self.get_source_url(message)

        image = io.imread(source_url)[:, :, :3]
        pil_image = Image.fromarray(image)
        string = image_to_string(pil_image)
        percentages = self.PERCENTAGE_RE.search(string).groups()
        if len(percentages) > 0:
            percentage = percentages[0]
            if percentage > 50:
                return f"You good. ({percentage}%)"
            else:
                return f"CHARGE YA GOTDAMN PHONE ({percentage}%)"
        else:
            return "No percentage found."
