import face_recognition
from PIL import Image, ImageDraw

image = face_recognition.load_image_file('jt.png')
pil_image = Image.fromarray(image)
draw = ImageDraw.Draw(pil_image)
faces = face_recognition.face_locations(image)
landmarks = face_recognition.face_landmarks(image)
for landmark in landmarks:
    draw.polygon(landmark['left_eye'], fill=(255, 255, 255, 20))

pil_image.save('out.png')
