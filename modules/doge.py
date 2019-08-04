from .base import ImageModule
from PIL import Image, ImageDraw, ImageFont
import random
import math


class Doge(ImageModule):
    DESCRIPTION = "Generate doge memes. So wow"
    ARGC = 1

    def rect_dist(self, a, b):
        ax0, ay0, ax1, ay1 = a
        bx0, by0, bx1, by1 = b
        width = max(0, max(ax0, bx0) - min(ax1, bx1))
        height = max(0, max(ay0, by0) - min(ay1, by1))
        return math.sqrt(width**2 + height**2)

    def response(self, query, message):
        words = self.lines(query)
        if len(words) == 1:
            words = query.split()
        decorators = ["so", "very", "much", "such"]
        words = [random.choice(decorators) + " " + word.lower() for word in words]

        font = ImageFont.truetype("resources/fonts/Comic Sans MS.ttf", 34, encoding="unic")
        image = Image.open("resources/doge.jpg")
        draw = ImageDraw.Draw(image)

        old_boxes = []
        colors = ["Red", "#7EFDFF", "Yellow", "Teal", "#ffbadd", "Brown", "Green", "DarkViolet", "DarkMagenta"]
        words.append("wow")
        gutter = 20

        for i, word in enumerate(words):
            box = None
            iterations = 0
            (text_width, text_height) = draw.textsize(word, font=font)
            while box is None:
                x = random.randint(gutter, image.size[0] - text_width - gutter)
                y = random.randint(gutter, image.size[1] - text_height - gutter)
                box = (x, y, x + text_width, y + text_height)

                iterations += 1
                if iterations > 100:
                    break
                for other in old_boxes:
                    dist = self.rect_dist(box, other)
                    if dist < 100:
                        box = None
                        break

            old_boxes.append(box)
            color = colors[i % len(colors)]

            draw.text((box[0], box[1]), word, font=font, fill=color)

        return self.upload_pil_image(image)
