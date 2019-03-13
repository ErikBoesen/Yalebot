import face_recognition
from PIL import Image, ImageDraw

image = face_recognition.load_image_file('jt.png')
pil_image = Image.fromarray(image)
uwu = Image.open('uwu.png')
draw = ImageDraw.Draw(pil_image)
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
