from .base import Module, ImageUploader
import face_recognition
from PIL import Image, ImageDraw
import requests
import os
from io import BytesIO
# TODO: skimage is so heavy for just using it for this...
from skimage import io
import math


class UWU(Module, ImageUploader):
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

        tear = Image.open("resources/uwu/tear.png")
        blush = Image.open("resources/uwu/blush.png")
        image = io.imread(source_url)[:, :, :3]
        # TODO: crashes if image is too large; need to use self.limit_image_size but that doesn't change `image` just PIL Images
        pil_image = Image.fromarray(image)
        faces = face_recognition.face_landmarks(image)
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
            pil_image.paste(scaled_blush, (int(blush_x - blush_width / 2), int(blush_y)), scaled_blush)
            pil_image.paste(scaled_tear, (int(left_tear_x - tear_width / 2), int(left_tear_y)), scaled_tear)
            pil_image.paste(scaled_tear, (int(right_tear_x - tear_width / 2), int(right_tear_y)), scaled_tear)

        """
        pil_image.show()
        return
        """
        return "", self.upload_pil_image(pil_image)


"""
avatar = "https://i.groupme.com/1023x1024.jpeg.1d34cf6dbad346b2b25bd8fbb2e71a97"
avatar = "https://i.groupme.com/750x704.jpeg.150575509d5e4449b9904faf3bb2ad10"
UWU().response("", {"avatar_url": avatar, "attachments": []})
"""
