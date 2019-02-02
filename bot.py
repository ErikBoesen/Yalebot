import os
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

app = Flask(__name__)
bot_id = "REPLACE THIS WITH YOUR BOT ID ONCE BOT IS ADDED TO THE CHAT"

@app.route("/", methods=["POST"])
def webhook():
    """
    Receive callback to URL when message is sent in the group.
    """
    # Retrieve data on that single GroupMe message.
    message = request.get_json()

    if "Can I get an f in the chat" in message["text"].lower() and not sender_is_bot(message):
        reply("f")

    return "ok", 200

def reply(msg):
    """
    Reply in chat.
    """
    url = "https://api.groupme.com/v3/bots/post"
    data = {
        "bot_id": bot_id,
        "text": msg
    }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()

# Checks whether the message sender is a bot
def sender_is_bot(message):
    return message["sender_type"] == "bot"
