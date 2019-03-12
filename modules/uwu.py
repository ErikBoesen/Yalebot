from .base import Module
import face_recognition
from PIL import Image, ImageDraw
import requests
import os
from io import BytesIO
# TODO: skimage is so heavy for just using it for this...
from skimage import io

class UWU(Module):
    DESCRIPTION = "Abuse photographs of your compatriots"
    def tear_position(self, element):
        # TODO: I feel like I shouldn't have to do this logic myself, but it does work ok.
        top = None
        left = None
        right = None
        for x, y in element:
            if top is None or top < y:
                top = y
            if left is None or left > x:
                left = x
            if right is None or right < x:
                right = x
        return (left + right) / 2, top

    def response(self, query, message):
        image_attachments = [attachment for attachment in message["attachments"] if attachment["type"] == "image"]
        if len(image_attachments) > 0:
            # Get sent image
            source_url = image_attachments[0]["url"]
        else:
            # If no image was sent, use sender's avatar
            source_url = message["avatar_url"]
        print("Image source URL: " + source_url)

        uwu = Image.open("resources/uwu/uwu.png")
        eye = Image.open("resources/uwu/eye.png")
        image = io.imread(source_url)[:,:,:3]
        pil_image = Image.fromarray(image)
        #faces = face_recognition.face_locations(image)
        faces = face_recognition.face_landmarks(image)
        print(faces);return
        if len(faces) == 0:
            return "No faces found in image."
        for face in faces:
            top, right, bottom, left = face

            # Scale uwu mask
            eye_natural_width, eye_natural_height = eye.size
            eye_width = int((right - left) * 0.7)
            eye_height = int(eye_width * eye_natural_height / eye_natural_width)
            scaled_eye = eye.resize((eye_width, eye_height), Image.ANTIALIAS)

            pil_image.paste(scaled_eye, (left + int(0.15 *1.0/0.7* eye_width), top + (bottom - top) // 4), scaled_eye)
        #pil_image.save("out.png")
        pil_image.imshow()
        return

        output = BytesIO()
        pil_image.save(output, format="JPEG")
        return "", self.upload_image(output.getvalue())

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

UWU().response("", {"avatar_url": "https://i.groupme.com/1023x1024.jpeg.1d34cf6dbad346b2b25bd8fbb2e71a97.large", "attachments": []})
