import modules
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
GROUP_ID = 1140136552771525
UNI_GROUPS = {
    'University of Michigan': 'https://groupme.com/join_group/46781389/hZehS1',
}

@app.route("/", methods=["POST"])
def webhook():
    """
    Receive callback to URL when message is sent in the group.
    """
    # Retrieve data on that single GroupMe message.
    message = request.get_json()
    text = message["text"]
    print("Message received: %s" % message)
    matches = F_PATTERN.match(message["text"])
    if matches is not None and len(matches.groups()):
        reply(matches.groups()[0] + ' ❤')
    if message["sender_type"] != "bot":
        if text.startswith("!"):
            command, parameters = text[1:].split(" ", 1)
            command = command.lower()
            module = {
                "zalgo": modules.Zalgo,
                "flip": modules.Flip,
                "countdown": modules.Countdown,
                "vet": modules.Vet,
                "bulldog": modules.Bulldog,
            }[command]()
            response = module.response()
            if response is not None:
                reply(response)
        if "thank" in message["text"].lower() and "yalebot" in message["text"].lower():
            reply("You're welcome! :)")
        if "favorite song" in message["text"].lower():
            reply(BOOLA_BOOLA)
        if "dad" in message["text"].lower():
            new_text = message["text"].strip().replace("dad", "dyd").replace("Dad", "Dyd").replace("DAD", "DYD")
            reply("Hey " + message["name"] + ", did you mean \"" + new_text + "\"?")
    if message["system"]:
        if not message["text"].startswith("Poll '") and message["text"].contains("the group") and not message.contains("changed name"):
            name = message["text"].replace(" has rejoined the group", "").replace(" has joined the group", "")
            reply(modules.Vet().check_user(name))
    return "ok", 200

def reply(text):
    """
    Reply in chat.
    """
    url = "https://api.groupme.com/v3/bots/post"
    data = {
        "bot_id": os.environ["BOT_ID"],
        "text": text,
    }
    request = Request(url, urlencode(data).encode())
    response = urlopen(request).read().decode()
    print("Response after message send: %s" % response)

if __name__ == "__main__":
    print(modules.Countdown().response())
    print(modules.Zalgo().response("Test zalgo"))
