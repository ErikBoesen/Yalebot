from .base import Module
import face_recognition
from PIL import Image, ImageDraw
import requests
import numpy as np

class UWU(Module):
    DESCRIPTION = 'Abuse photographs of your compatriots'
    uwu = Image.open('uwu.png')
    draw = ImageDraw.Draw(pil_image)
    def response(self, query, message):
        # Get sent image
        source_url = [attachment for attachment in message['attachments'] if attachment['type'] == 'image'][0].get('image')
        # If no image was sent, use sender's avatar
        source_url = source_url or attachment['avatar_url']

        r = requests.get(source_url)
        raw_image = r.text
        pil_image = Image.frombytes(raw_image)
        faces = face_recognition.face_locations(image)
        for face in faces:
            top, right, bottom, left = face

            # Scale uwu mask
            width, height = uwu.size
            uwu_width = int((right - left) * 0.6)
            uwu_height = int(uwu_width * height / width)
            uwu = uwu.resize((uwu_width, uwu_height), Image.ANTIALIAS)

            pil_image.paste(uwu, (left + int(0.2 *1.0/0.6* uwu_width), top + (bottom - top) // 5), uwu)

        pil_image.save('out.png')

if __name__ == '__main__':
    print(UWU.response('', {'attachments': [{'type': 'image', 'url': 'https://i.groupme.com/1296x972.jpeg.91ab436782064b278a647dd7cf924c81.preview'}]}))
