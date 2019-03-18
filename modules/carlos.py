from .base import Module, ImageUploader
from PIL import Image, ImageDraw
import random
from io import BytesIO
# TODO: This is so complicated for literally just reading an image from a URL
from skimage import io

class Carlos(Module, ImageUploader):
    DESCRIPTION = "❤️"
    hearts = [Image.open(f"resources/hearts/{number}.png") for number in range(0, 11+1)]
    HEART_RESOLUTION = 120
    def response(self, query, message):
        source_url = self.get_source_url(message)

        image = io.imread(source_url)[:,:,:3]
        pil_image = Image.fromarray(image)
        image_width, image_height = pil_image.size
        for heart in self.hearts:
            heart_size = random.randint(image_height // 6, image_height // 4)
            processed_heart = heart.resize((heart_size, heart_size), Image.ANTIALIAS).rotate(random.randint(0, 360))
            pil_image.paste(processed_heart,
                            (int(random.random() * (image_width - heart_size)), int(random.random() * (image_height - heart_size))),
                            processed_heart)

        output = BytesIO()
        pil_image.save(output, format="JPEG")
        return "", self.upload_image(output.getvalue())
