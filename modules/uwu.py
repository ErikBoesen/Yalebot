from .base import Module
import face_recognition
from PIL import Image, ImageDraw
import requests
import os
from io import BytesIO
# TODO: skimage is so heavy for just using it for this...
from skimage import io

class UWU(Module):
    DESCRIPTION = 'Abuse photographs of your compatriots'
    uwu = Image.open('resources/uwu.png')
    def response(self, query, message):
        # Get sent image
        source_url = [attachment for attachment in message['attachments'] if attachment['type'] == 'image'][0].get('url')
        # If no image was sent, use sender's avatar
        source_url = source_url or message['avatar_url']

        image = io.imread(source_url)
        pil_image = Image.fromarray(image)
        faces = face_recognition.face_locations(image)
        if len(faces) == 0:
            return 'No faces found in image.'
        for face in faces:
            top, right, bottom, left = face

            # Scale uwu mask
            width, height = self.uwu.size
            uwu_width = int((right - left) * 0.6)
            uwu_height = int(uwu_width * height / width)
            scaled_uwu = self.uwu.resize((uwu_width, uwu_height), Image.ANTIALIAS)

            pil_image.paste(scaled_uwu, (left + int(0.2 *1.0/0.6* uwu_width), top + (bottom - top) // 5), scaled_uwu)
        #pil_image.save('out.png')
        output = BytesIO()
        pil_image.save(output, format="JPEG")
        return self.upload_image(output.getvalue())

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
