import modules
import os
import re
import requests
import json
import difflib
from flask import Flask, request


app = Flask(__name__)
with open("groups.json", "r") as f:
    GROUPS = json.load(f)

MAX_MESSAGE_LENGTH = 1000
PREFIX = "!"

static_commands = {
    "ping": "Pong!",
    "sam": "❗❗❗N O 💪 F L E X 💪 Z O N E ❗❗❗",
    "essays": "Submit your essays here, or read your classmates'! https://drive.google.com/open?id=1IUG1cNxmxBHhv1sSemi92fYO6y5lG6of",
    "spreadsheet": "https://docs.google.com/spreadsheets/d/10m_0glWVUncKCxERsNf6uOJhfeYU96mOK0KvgNURIBk/edit?fbclid=IwAR35OaPO6czQxZv26A6DEgEH-Qef0kCSe4nXxl8wcIfDml-BfLx4ksVtp6Y#gid=0",
    "meetup": ("", "https://i.groupme.com/750x1200.jpeg.b0ca5f6e660a4356be2925222e6f8246.large"),
    "quack": "quack",
    "test": "https://erikboesen.com/yalepuritytest",
    "dislike": "👎😬👎\n 🦵🦵",
    "shrug": r"¯\_(ツ)_/¯",
    "snort": "😤",
    "oh": ("", "https://i.groupme.com/766x750.jpeg.9209520c57e848369444ca498e31f90a.large"),
    "bulldog": "Bulldog!  Bulldog!\nBow, wow, wow\nEli Yale\nBulldog!  Bulldog!\nBow, wow, wow\nOur team can never fail\n\nWhen the sons of Eli\nBreak through the line\nThat is the sign we hail\nBulldog!  Bulldog!\nBow, wow, wow\nEli Yale!",
    "popcorn": "https://www.youtube.com/watch?v=9nwOm4AAXwc",
    "yyle": "https://www.youtube.com/watch?v=SsZDxL-YMYc",
}

commands = {
    "zalgo": modules.Zalgo(),
    "flip": modules.Flip(),
    "countdown": modules.Countdown(),
    "verify": modules.Verify(),
    "mccarthy": modules.McCarthy(),
    "groups": modules.Groups(),
    "about": modules.About(),
    "xkcd": modules.XKCD(),
    "elizabeth": modules.Elizabeth(),
    "dania": modules.Dania(),
    "jake": modules.Jake(),
    "carlos": modules.Carlos(),
    "crista": modules.Crista(),
    "maria": modules.Maria(),
    "annie": modules.Annie(),
    "chat": modules.Chat(),
    "weather": modules.Weather(),
    "kelly": modules.Kelly(),
    "sad": modules.Sad(),
    "eightball": modules.EightBall(),
    "analytics": modules.Analytics(),
    "youtube": modules.YouTube(),
    "pick": modules.Pick(),
    "chose": modules.Chose(),
    "meme": modules.Meme(),
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
    "funny": modules.Funny(),
    "kelbo": modules.Kelbo(),
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
            instructions = text[len(PREFIX):].strip().split(" ", 1)
            command = instructions.pop(0).lower()
            query = instructions[0] if len(instructions) > 0 else ""
            # Check if there's an automatic response for this command
            if command in static_commands:
                reply(static_commands[command], group_id)
            # If not, query appropriate module for a response
            elif command in commands:
                # Make sure there are enough arguments
                if len(list(filter(None, query.split("\n")))) < commands[command].ARGC:
                    reply("Not enough arguments!", group_id)
                else:
                    response = commands[command].response(query, message)
                    if response is not None:
                        reply(response, group_id)
            elif command == "help":
                if query:
                    query = query.strip(PREFIX)
                    if query in static_commands:
                        reply(PREFIX + query + ": static response.", group_id)
                    elif query in commands:
                        reply(PREFIX + query + ": " + commands[query].DESCRIPTION + f". Requires {commands[query].ARGC} argument(s).", group_id)
                    elif query in meme_commands:
                        reply(PREFIX + query + ": meme command; provide captions separated by newlines.", group_id)
                    else:
                        reply("No such command.", group_id)
                else:
                    help_string = "--- Help ---"
                    help_string += "\nStatic commands: " + ", ".join([PREFIX + title for title in static_commands])
                    help_string += "\nTools: " + ", ".join([PREFIX + title for title in commands])
                    help_string += f"\n(Run `{PREFIX}help commandname` for in-depth explanations.)"
                    reply(help_string, group_id)
            else:
                try:
                    closest = difflib.get_close_matches(command, list(static_commands.keys()) + list(commands.keys()), 1)[0]
                    advice = f"Perhaps you meant {PREFIX}{closest}? "
                except IndexError:
                    advice = ""
                reply(f"Command not found. {advice}Use !help to view a list of commands.", group_id)

        if H_PATTERN.search(text) is not None:
            reply(forename + ", did you mean \"" + H_PATTERN.sub("H******", text) + "\"? Perhaps you meant to say \"" + H_PATTERN.sub("The H Place", text) + "\" instead?", group_id)
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
            check_names = system_responses["welcome"].get_names(text)
            for check_name in check_names:
                reply(commands["vet"].check_user(check_name), group_id)
        """
    return "ok", 200


def reply(message, group_id):
    """
    Reply in chat.
    :param message: text of message to send. May be a tuple with further data, or a list of messages.
    :param group_id: ID of group in which to send message.
    """
    # Recurse to send a list of messages.
    # This is useful when a module must respond with multiple messages.
    # TODO: This feels sort of clunky.
    if isinstance(message, list):
        for item in message:
            reply(item, group_id)
        return
    data = {
        "bot_id": GROUPS[group_id]["bot_id"],
    }
    if isinstance(message, tuple):
        text, image = message
    else:
        text = message
        image = None
    if len(text) > MAX_MESSAGE_LENGTH:
        # If text is too long for one message, split it up over several
        for block in [text[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]:
            reply(block, group_id)
        data["text"] = ""
    else:
        data["text"] = text
    if image is not None:
        data["picture_url"] = image
    # Prevent sending message if there's no content
    # It would be rejected anyway
    if data["text"] or data["picture_url"]:
        response = requests.post("https://api.groupme.com/v3/bots/post", data=data)
