from .base import ImageModule
from PIL import Image, ImageDraw, ImageFont


class Damn(ImageModule):
    DESCRIPTION = "Mimic the DAMN. album cover. Send an image and/or specify a caption."
    ARGC = 0

    def transform(self, text):
        if not text:
            return "DAMN."
        return text.strip(".").upper() + "."

    def response(self, query, message):
        query = self.transform(query)
        source_url = self.get_source_url(message, include_avatar=False)
        if source_url is None:
            background = Image.open("resources/damn.jpg")
        else:
            background = self.pil_from_url(source_url)
        background_width, background_height = background.size
        draw_background = ImageDraw.Draw(background)

        font_size = background_width
        font = ImageFont.truetype("resources/fonts/times.ttf", font_size)
        words = Image.new("RGBA", draw_background.textsize(query, font=font))
        draw_words = ImageDraw.Draw(words)
        draw_words.text((0, 0), query, font=font, fill=(255, 0, 0))
        # We need to trim off the top of the image because the font has padding
        words_width, words_height = words.size
        words = words.crop((0, int(font_size * .20), words_width, words_height))
        # Resize to fit width of background
        words = self.resize(words, background_width)

        # Superimpose text
        background.paste(words, (0, 0), words)
        background.show()
