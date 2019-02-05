from PIL import Image, ImageFont, ImageDraw
from textwrap import wrap
import requests
import os
import io


class Drake:
    FONT_SIZE = 30
    BLACK = (0, 0, 0)
    def __init__(self):
        self.template = Image.open("resources/memes/drake.jpg")
        self.font = ImageFont.truetype("resources/Lato-Regular.ttf", self.FONT_SIZE)

    def response(self, query):
        image = self.template
        left_border = 330
        right_border = 620

        captions = query.split("\n")
        draw = ImageDraw.Draw(image)

        START_Y = 100
        for caption_index, caption in enumerate(captions):
            lines = wrap(caption, 20)
            for line_index, line in enumerate(lines):
                draw.text((left_border + 20, 80 * (caption_index + 1)**2 + self.FONT_SIZE * 1.3 * line_index), line, font=self.font, fill=self.BLACK)

        output = io.BytesIO()
        image.save(output, format="JPEG")
        image_url = self.upload_image(output.getvalue())
        return image_url

    def upload_image(self, data) -> str:
        """
        Send image to GroupMe Image API.

        :param data: compressed image data.
        :return: URL of image now hosted on GroupMe server.
        """
        headers = {
            "X-Access-Token": os.environ["GROUPME_ACCESS_TOKEN"],
            "Content-Type": "image/jpeg",
        }
        r = requests.post("https://image.groupme.com/pictures", data=data, headers=headers)
        return r.json()["payload"]["url"]
