from .base import Module, ImageUploader
from PIL import Image, ImageDraw
import random
from io import BytesIO
# TODO: This is so complicated for literally just reading an image from a URL
from skimage import io

class Carlos(Module, ImageUploader):
    DESCRIPTION = "❤️"
    hearts = [Image.open(f"resources/hearts/{number}.png") for number in range(0, 13+1)]
    HEART_RESOLUTION = 120
    def response(self, query, message):
        heart_count = query.split(" ", 1)[0]
        try:
            heart_count = int(heart_count)
        except:
            heart_count = len(self.hearts)
        source_url = self.get_source_url(message)

        image = io.imread(source_url)[:,:,:3]
        pil_image = Image.fromarray(image)
        image_width, image_height = pil_image.size
        for heart_number in range(heart_count):
            heart = self.hearts[heart_number % len(self.hearts)]
            heart_size = random.randint(image_height // 6, image_height // 4)
            processed_heart = heart.resize((heart_size, heart_size), Image.ANTIALIAS).rotate(random.randint(0, 360), expand=True)
            processed_width, processed_height = processed_heart.size
            pil_image.paste(processed_heart,
                            (int(random.random() * (image_width - processed_width)), int(random.random() * (image_height - processed_height))),
                            processed_heart)

        output = BytesIO()
        pil_image.save(output, format="JPEG")
        return "", self.upload_image(output.getvalue())
