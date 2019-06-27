from .base import ImageModule
from PIL import Image, ImageDraw
import random


class Shield(ImageModule):
    DESCRIPTION = "Superimpose your residential college shield on a photo/"
    hearts = [Image.open(f"resources/hearts/{number}.png") for number in range(0, 13 + 1)]

    def response(self, query, message):
        background = self.pil_from_url(source_url)
        shield_width, shield_height = background.size
        shield_width //= 5
        shield_height //= 5

        for heart_number in range(heart_count):
            heart = self.hearts[heart_number % len(self.hearts)]
            heart_size = random.randint(image_height // 6, image_height // 4)
            processed_heart = heart.resize((heart_size, heart_size), Image.ANTIALIAS).rotate(random.randint(0, 360), expand=True)
            processed_width, processed_height = processed_heart.size
            background.paste(processed_heart,
                             (int(random.random() * (image_width - processed_width)), int(random.random() * (image_height - processed_height))),
                             processed_heart)

        return "", self.upload_pil_image(background)
