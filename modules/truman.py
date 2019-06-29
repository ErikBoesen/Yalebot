from .base import ImageModule
import re
import ocrspace


class Truman(ImageModule):
    DESCRIPTION = "Is your battery sinfully low?"
    PERCENTAGE_RE = re.compile(r"(\d+) *%")
    api = ocrspace.API()

    def response(self, query, message):
        source_url = self.get_source_url(message)
        string = self.api.ocr_url(source_url)
        print("Image text: " + string)
        string = string.replace("0/0", "%")
        percentages = self.PERCENTAGE_RE.search(string).groups()
        if len(percentages) > 0:
            percentage = int(percentages[0])
            if percentage > 50:
                return f"You good. ({percentage}%)"
            else:
                return f"CHARGE YA GOTDAMN PHONE ({percentage}%)"
        else:
            return "No percentage found."
