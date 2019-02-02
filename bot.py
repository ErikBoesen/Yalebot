import os
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

app = Flask(__name__)
with open("config.json", "r") as f:
    config = json.load(f)

@app.route("/", methods=["POST"])
def webhook():
    """
    Receive callback to URL when message is sent in the group.
    """
    # Retrieve data on that single GroupMe message.
    message = request.get_json()
    if "Can I get an f in the chat" in message["text"] and message["sender_type"] != "bot":
        reply("f")
    return "ok", 200

def reply(text):
    """
    Reply in chat.
    """
    url = "https://api.groupme.com/v3/bots/post"
    data = {
        "bot_id": config["id"],
        "text": text,
    }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()
