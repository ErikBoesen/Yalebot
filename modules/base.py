import os

class Module:
    DESCRIPTION = ""
    ARGC = 0
    ACCESS_TOKEN = os.environ["GROUPME_ACCESS_TOKEN"]
    def __init__(self):
        print("Loaded module %s." % self.__class__.__name__)

class ImageUploader:
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
