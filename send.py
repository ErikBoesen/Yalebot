import requests
import os

text = input('Message: ')
requests.post("https://api.groupme.com/v3/bots/post", data={"text": text, "bot_id": os.environ["BOT_ID"]})

