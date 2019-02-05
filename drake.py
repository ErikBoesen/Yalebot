from PIL import Image, ImageFont, ImageDraw
from textwrap import wrap

im = Image.open("resources/memes/drake.jpg")
FONT_SIZE = 30
font = ImageFont.truetype("resources/Lato-Regular.ttf", FONT_SIZE)

BLACK = (0, 0, 0)

left_border = 330
right_border = 620

captions = ["statement", "Can I get a statement in the chat"]
draw = ImageDraw.Draw(im)

START_Y = 100
for caption_index, caption in enumerate(captions):
    lines = wrap(caption, 20)
    for line_index, line in enumerate(lines):
        draw.text((left_border + 20, 80 * (caption_index + 1)**2 + FONT_SIZE * 1.3 * line_index), line, font=font, fill=BLACK)

import requests
import os
import io

output = io.BytesIO()
im.save(output, format='JPEG')
headers = {
    "X-Access-Token": os.environ["GROUPME_ACCESS_TOKEN"],
    "Content-Type": "image/jpeg",
}
#    "image": output.getvalue()
raw=  open("resources/memes/drake.jpg", "rb")
r = requests.post("https://image.groupme.com/pictures", data=raw, headers=headers)
print(r.json())

#im.show()

