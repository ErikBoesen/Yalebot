from PIL import Image, ImageFont
im = Image.open("resources/memes/drake.jpg")
font = ImageFont.truetype("resources/Lato-Regular.ttf", 16)

left_border = 330
right_border = 620

im.show()

