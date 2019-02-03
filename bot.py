import os
import json
import re
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request
import facebook

app = Flask(__name__)
F_PATTERN = re.compile('can i get an? (.+) in the chat', flags=re.IGNORECASE | re.MULTILINE)
SUFFIX = '❤️'
GROUP_ID = 1140136552771525

@app.route("/", methods=["POST"])
def webhook():
    """
    Receive callback to URL when message is sent in the group.
    """
    # Retrieve data on that single GroupMe message.
    message = request.get_json()
    print("Message received: %s" % message)
    if message["sender_type"] != "bot":
        matches = F_PATTERN.match(message["text"])
        if matches is not None and len(matches.groups()):
            reply(matches.groups()[0] + ' ' + SUFFIX)
        if message["text"] == "YO":
            reply("", image="https://i.groupme.com/1200x1500.jpeg.de46caa3987c440ea9f4c0b1513278d3.large")
    if message["system"]:
        print("System message!")

    return "ok", 200

def reply(text, image=None):
    """
    Reply in chat.
    """
    url = "https://api.groupme.com/v3/bots/post"
    data = {
        "bot_id": os.environ["BOT_ID"],
        "text": text,
    }
    if image is not None:
        data["attachments"] = [{"type": "image",
                                "url": image}]
    request = Request(url, urlencode(data).encode())
    response = urlopen(request).read().decode()
    print("Response after message send: %s" % response)

def vet_user(name: str):
    """
    Check Facebook to determine if user is part of the Yale '23 group.
    """
    os.environ['FACEBOOK_TOKEN']

