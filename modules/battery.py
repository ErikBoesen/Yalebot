from PIL import Image
from pytesseract import image_to_string

print(image_to_string(Image.open('/home/erik/ss.png')))

