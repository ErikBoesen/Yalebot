from .base import Module, ImageUploader
from PIL import Image, ImageDraw
import random
# TODO: This is so complicated for literally just reading an image from a URL
from skimage import io


class Carlos(Module, ImageUploader):
    DESCRIPTION = "❤️"
    hearts = [Image.open(f"resources/hearts/{number}.png") for number in range(0, 13 + 1)]
    HEART_RESOLUTION = 120
    MAX_HEARTS = 2000

    def response(self, query, message):
        heart_count = query.split(" ", 1)[0]
        try:
            heart_count = int(heart_count)
            heart_count = min(heart_count, self.MAX_HEARTS)
        except ValueError:
            heart_count = len(self.hearts)
        source_url = self.get_source_url(message)

        background = self.pil_from_url(source_url)
        image_width, image_height = background.size
        for heart_number in range(heart_count):
            heart = self.hearts[heart_number % len(self.hearts)]
            heart_size = random.randint(image_height // 6, image_height // 4)
            processed_heart = heart.resize((heart_size, heart_size), Image.ANTIALIAS).rotate(random.randint(0, 360), expand=True)
            processed_width, processed_height = processed_heart.size
            background.paste(processed_heart,
                             (int(random.random() * (image_width - processed_width)), int(random.random() * (image_height - processed_height))),
                             processed_heart)

        return "", self.upload_pil_image(background)
