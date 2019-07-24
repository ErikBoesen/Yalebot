from .base import ImageModule
import face_recognition
from PIL import Image, ImageDraw
import math
import numpy as np


class UWU(ImageModule):
    DESCRIPTION = "Abuse photographs of your compatriots"

    def tear_position(self, element):
        top = None
        bottom = None
        left = None
        right = None
        for x, y in element:
            if bottom is None or bottom < y:
                bottom = y
            if top is None or top > y:
                top = y
            if left is None or left > x:
                left = x
            if right is None or right < x:
                right = x
        return (left + right) / 2, top

    def response(self, query, message):
        source_url = self.get_source_url(message)
        background = self.pil_from_url(source_url)
        background = self.rotate_upright(background)
        background = self.limit_image_size(background)

        tear = Image.open("resources/uwu/tear.png")
        blush = Image.open("resources/uwu/blush.png")
        faces = face_recognition.face_landmarks(np.array(background))
        if len(faces) == 0:
            return "No faces found in image."
        for face in faces:
            left_tear_x, left_tear_y = self.tear_position(face["left_eye"])
            right_tear_x, right_tear_y = self.tear_position(face["right_eye"])

            # Scale tear mask
            tear_natural_width, tear_natural_height = tear.size
            tear_width = int(math.sqrt((right_tear_x - left_tear_x)**2 + (right_tear_y - left_tear_y)**2) * 0.4)
            tear_height = int(tear_width * tear_natural_height / tear_natural_width)
            scaled_tear = tear.resize((tear_width, tear_height), Image.ANTIALIAS)

            # Center blush between eyes
            blush_x = (left_tear_x + right_tear_x) / 2
            # Position blush based on tear position (easier than alternatives)
            blush_y = (left_tear_y + right_tear_y) / 2 + tear_height / 4

            # Scale blush mask
            blush_natural_width, blush_natural_height = blush.size
            blush_height = int(tear_height * 0.35)
            blush_width = int(blush_height * blush_natural_width / blush_natural_height)
            scaled_blush = blush.resize((blush_width, blush_height), Image.ANTIALIAS)

            # Actually draw blush and tears
            background.paste(scaled_blush, (int(blush_x - blush_width / 2), int(blush_y)), scaled_blush)
            background.paste(scaled_tear, (int(left_tear_x - tear_width / 2), int(left_tear_y)), scaled_tear)
            background.paste(scaled_tear, (int(right_tear_x - tear_width / 2), int(right_tear_y)), scaled_tear)

        return "", self.upload_pil_image(background)
