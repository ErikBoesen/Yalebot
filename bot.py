import modules
import os
import re
import requests
import json
from flask import Flask, request


app = Flask(__name__)
with open("groups.json", "r") as f:
    GROUPS = json.load(f)

MAX_MESSAGE_LENGTH = 1000
PREFIX = "!"

simple_responses = {
    "ping": "Pong!",
    "about": f"I am a bot maintained by Erik Bøsen, whom you should follow on Instagram @erikboesen. Use the command {PREFIX}help to view a list of bot capabilities. The bot's source code can be viewed and contributed to on GitHub: https://github.com/ErikBoesen/Yalebot",
    "sam": "❗❗❗N O 💪 F L E X 💪 Z O N E ❗❗❗",
    "essays": "Submit your essays here, or read your classmates'! https://drive.google.com/open?id=1IUG1cNxmxBHhv1sSemi92fYO6y5lG6of",
    "spreadsheet": "https://docs.google.com/spreadsheets/d/10m_0glWVUncKCxERsNf6uOJhfeYU96mOK0KvgNURIBk/edit?fbclid=IwAR35OaPO6czQxZv26A6DEgEH-Qef0kCSe4nXxl8wcIfDml-BfLx4ksVtp6Y#gid=0",
    "meetup": "https://i.groupme.com/750x1200.jpeg.b0ca5f6e660a4356be2925222e6f8246.large",
    "quack": "quack",
    "test": "https://erikboesen.com/yalepuritytest",
    "dislike": "👎😬👎\n 🦵🦵",
    "shrug": "¯\_(ツ)_/¯",
    "snort": "😤",
    "oh": "https://i.groupme.com/766x750.jpeg.9209520c57e848369444ca498e31f90a.large",
}
commands = {
    "zalgo": modules.Zalgo(),
    "flip": modules.Flip(),
    "countdown": modules.Countdown(),
    "vet": modules.Vet(),
    "bulldog": modules.Bulldog(),
    "groups": modules.Groups(),
    "chat": modules.Chat(),
    "weather": modules.Weather(),
    "kelly": modules.Kelly(),
    "sad": modules.Sad(),
    "eightball": modules.EightBall(),
    "analytics": modules.Analytics(),
    "youtube": modules.YouTube(),
    "pick": modules.Pick(),
    "chose": modules.Chose(),
    "love": modules.Love(),
    "price": modules.Price(),
    "minion": modules.Minion(),
    "house": modules.House(),
    "location": modules.Location(),
    "twitter": modules.Twitter(),
    "tea": modules.Tea(),
    "lyrics": modules.Lyrics(),
    "nasa": modules.NASA(),
    "amber": modules.Amber(),
    "uwu": modules.UWU(),
    "conversationstarter": modules.ConversationStarter(),
    "quote": modules.Quote(),
    "dog": modules.Dog(),
    "funfact": modules.FunFact(),
}
meme_commands = {
    "drake": modules.Drake(),
    "ydrake": modules.YaleDrake(),
    "juice": modules.Juice(),
    "changemymind": modules.ChangeMyMind(),
    "catch": modules.Catch(),
    "kirby": modules.Kirby(),
}
system_responses = {
    "welcome": modules.Welcome(),
}

F_PATTERN = re.compile("can i get an? (.+) in the chat", flags=re.IGNORECASE | re.MULTILINE)
H_PATTERN = re.compile("(harvard)", flags=re.IGNORECASE)
@app.route("/", methods=["POST"])
def webhook():
    """
    Receive callback to URL when message is sent in the group.
    """
    # Retrieve data on that single GroupMe message.
    message = request.get_json()
    group_id = message["group_id"]
    text = message["text"]
    name = message["name"]
    forename = name.split(" ", 1)[0]
    print("Message received: %s" % message)
    matches = F_PATTERN.search(text)
    if matches is not None and len(matches.groups()):
        reply(matches.groups()[0] + " ❤", group_id)
    if message["sender_type"] != "bot":
        if text.startswith(PREFIX):
            instructions = text[len(PREFIX):].split(" ", 1)
            command = instructions.pop(0).lower()
            query = instructions[0] if len(instructions) > 0 else ""
            # Check if there's an automatic response for this command
            if command in simple_responses:
                reply(simple_responses[command], group_id)
            # If not, query appropriate module for a response
            elif command in commands:
                # Make sure there are enough arguments
                if len(list(filter(None, query.split("\n")))) < commands[command].ARGC:
                    reply("Not enough arguments!", group_id)
                else:
                    response = commands[command].response(query, message)
                    if response is not None:
                        reply(response, group_id)
            elif command in meme_commands:
                # TODO: This is clumsy logic. First of all it's done twice, first in the normal commands
                # section, and then again here. Second, meme commands split the query into lines
                # already; we're just doing it twice with this.
                if len(list(filter(None, query.split("\n")))) < meme_commands[command].ARGC:
                    reply("Not enough captions (make sure to separate with newlines).", group_id)
                else:
                    #reply("@" + message["name"], group_id, image=meme_commands[command].response(query))
                    reply(meme_commands[command].response(query), group_id)
            elif command == "help":
                if query:
                    query = query.strip(PREFIX)
                    if query in simple_responses:
                        reply(PREFIX + query + ": static command", group_id)
                    elif query in commands:
                        reply(PREFIX + query + ": " + commands[query].DESCRIPTION + f". Requires {commands[query].ARGC} arguments.", group_id)
                    elif query in meme_commands:
                        reply(PREFIX + query + ": meme command; provide captions separated by newlines.", group_id)
                    else:
                        reply("No such command.", group_id)
                else:
                    help_string = "--- Help ---"
                    help_string += "\nSimple commands: " + ", ".join([PREFIX + title for title in simple_responses])
                    help_string += "\nTools: " + ", ".join([PREFIX + title for title in commands])
                    help_string += f"\n(Run `{PREFIX}help commandname` for in-depth explanations.)"
                    help_string += "\n\nMemes: " + ", ".join([PREFIX + title for title in meme_commands])
                    reply(help_string, group_id)
            else:
                reply("Command not found. Use !help to view a list of commands.", group_id)

        if text.startswith("@Yalebot "):
            reply(commands["chat"].response(text.split(" ", 1)[1], message), group_id)
        if H_PATTERN.search(text) is not None:
            reply(forename + ", did you mean \"" + H_PATTERN.sub("H******", text) + "\"? Perhaps you meant to say \"" + H_PATTERN.sub("The H Place", text) + "\" instead?", group_id)
        if "prize" in text.lower():
            reply("stop", group_id)
        if "thank" in text.lower() and "yalebot" in text.lower():
            reply("You're welcome, " + forename + "! :)", group_id)
        if "dad" in text.lower():
            new_text = text.strip().replace("dad", "dyd").replace("Dad", "Dyd").replace("DAD", "DYD")
            reply("Hey " + forename + ", did you mean \"" + new_text + "\"?", group_id)
    if message["system"]:
        for option in system_responses:
            if system_responses[option].RE.match(text):
                reply(system_responses[option].response(), group_id)
        """
        if system_responses["welcome"].RE.match(text):
            check_name = system_responses["welcome"].get_name(text)
            reply(commands["vet"].check_user(check_name), group_id)
        """
    return "ok", 200

def send_message(data):
    """
    Send raw message data, without pre-processing.
    """
    response = requests.post("https://api.groupme.com/v3/bots/post", data=data)

def reply(message, group_id):
    """
    Reply in chat.
    :param message: text of message to send. May be a tuple with further data.
    :param group_id: ID of group in which to send message.
    """
    data = {
        "bot_id": GROUPS[group_id]["bot_id"],
    }
    # TODO: This is less than ideal.
    if isinstance(message, tuple):
        text = message[0]
        image = message[1]
    else:
        text = message
        image = None
    if len(text) > MAX_MESSAGE_LENGTH:
        # If text is too long for one message, split it up over several
        for block in [text[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]:
            data["text"] = block
            send_message(data)
        data["text"] = ""
    if image is not None:
        data["picture_url"] = image
    send_message(data)
