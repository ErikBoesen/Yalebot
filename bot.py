# Flask
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

# Other
import mebots
from threading import Thread
import requests
import os
import time
import re
import difflib
import argparse

# Bot components
from config import Config
from utils import Message, SenderType
from commands import static_commands, commands, system_commands, modules


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
cache = Cache(app, config={"CACHE_TYPE": "simple"})
bot = mebots.Bot("yalebot", os.environ.get("BOT_TOKEN"))

MAX_MESSAGE_LENGTH = 1000
PREFIX = "!"
CACHE_TIMEOUT = 60 * 60


# Database models
class Response(db.Model):
    __tablename__ = "responses"
    name = db.Column(db.String(64), primary_key=True)
    content = db.Column(db.String(256))
    image_url = db.Column(db.String(128))


# Backwards compatibility
@app.route("/manager")
def manager():
    return redirect("http://mebots.co/manager/yalebot")

# Webhook receipt and response
@app.route("/", methods=["POST"])
def receive():
    """
    Receive callback to URL when message is sent in the group.
    """
    # Retrieve data on that single GroupMe message.
    message = request.get_json()
    group_id = message["group_id"]
    # Begin reply process in a new thread.
    # This way, the request won't time out if a response takes too long to generate.
    Thread(target=reply, args=(message, group_id)).start()
    return "ok", 200


def reply(message, group_id):
    send(process_message(Message(message)), group_id)


def process_message(message):
    responses = []
    forename = message.name.split(" ", 1)[0]
    f_matches = re.search("can i get an? (.+) in the chat", message.text, flags=re.IGNORECASE | re.MULTILINE)
    if f_matches is not None and len(f_matches.groups()):
        responses.append(f_matches.groups()[0] + " ❤")
    if message.sender_type == SenderType.USER:
        if message.text.startswith(PREFIX):
            instructions = message.text[len(PREFIX):].strip().split(None, 1)
            command = instructions.pop(0).lower()
            query = instructions[0] if len(instructions) > 0 else ""
            # Prevent response if prefix is repeated
            if PREFIX in command:
                pass
            # Check if there's a static response for this command
            elif command in static_commands:
                responses.append(static_commands[command])
            # If not, query appropriate module for a response
            elif command in commands:
                # Make sure there are enough arguments
                if len(modules.Module.lines(None, query)) < commands[command].ARGC:
                    responses.append(commands[command].ARGUMENT_WARNING)
                else:
                    response = commands[command].response(query, message)
                    if response is not None:
                        responses.append(response)
            elif command == "help":
                if query:
                    query = query.strip(PREFIX)
                    if query in static_commands:
                        responses.append(PREFIX + query + ": static response.")
                    elif query in commands:
                        responses.append(PREFIX + query + ": " + commands[query].DESCRIPTION + f". Requires {commands[query].ARGC} argument(s).")
                    else:
                        responses.append("No such command.")
                else:
                    help_string = "--- Help ---"
                    help_string += "\nStatic commands: " + ", ".join([PREFIX + title for title in static_commands])
                    help_string += "\nTools: " + ", ".join([PREFIX + title for title in commands])
                    help_string += f"\n(Run `{PREFIX}help commandname` for in-depth explanations.)"
                    responses.append(help_string)
            elif command == "register":
                # TODO: this is lazy and bad, fix it
                args = query.split(None, 1)
                new_command = args.pop(0).lower()
                content = None
                if args:
                    content = args[0]
                response = Response.query.get(new_command)
                if response is None:
                    if not content and not message.image_url:
                        responses.append("Please provide content or an image.")
                    else:
                        response = Response(name=new_command, content=content, image_url=message.image_url)
                        db.session.add(response)
                        db.session.commit()
                        responses.append(f"Command {new_command} registered successfully.")
                else:
                    responses.append(f"Command {new_command} already registered!")
            elif command == "unregister":
                response = Response.query.get(query)
                if response is None:
                    responses.append(f"No registered command named {query}.")
                else:
                    db.session.delete(response)
                    db.session.commit()
                    responses.append(f"Command {query} unregistered.")
                """
                elif command == "stats":
                    count = Bot.query.count()
                    responses.append(f"I am currently in {count} GroupMe groups. Add me to more at https://yalebot.herokuapp.com!")
                """
            else:
                response = Response.query.get(command)
                if response is not None:
                    responses.append((response.content, response.image_url) if response.image_url else response.content)
                else:
                    try:
                        closest = difflib.get_close_matches(command, list(static_commands.keys()) + list(commands.keys()), 1)[0]
                        advice = f"Perhaps you meant {PREFIX}{closest}? "
                    except IndexError:
                        advice = ""
                    responses.append(f"Command not found. {advice}Use !help to view a list of commands.")
        if "netid" in message.text.lower().replace(" ","").replace("-",""):
            with open("resources/netID.txt", "r") as f: 
                 responses.append(f.read())
        if "thank" in message.text.lower() and "yalebot" in message.text.lower():
            responses.append("You're welcome, " + forename + "! :)")
    if message.sender_type == SenderType.SYSTEM:
        for option in system_commands:
            if system_commands[option].RE.match(message.text):
                responses.append(system_commands[option].response(message.text, message))
        """
        if system_commands["welcome"].RE.match(message.text):
            check_names = system_commands["welcome"].get_names_groupme(message.text)
            for check_name in check_names:
                responses.append(commands["verify"].check_user(check_name))
        """
    return responses


def send(message, group_id):
    """
    Reply in chat.
    :param message: text of message to send. May be a tuple with further data, or a list of messages.
    :param group_id: ID of group in which to send message.
    """
    # Recurse when sending multiple messages.
    if isinstance(message, list):
        for item in message:
            send(item, group_id)
        return
    data = {
        "bot_id": bot.instance(group_id).id,
    }
    image = None
    if isinstance(message, tuple):
        message, image = message
    # TODO: this is lazy
    if message is None:
        message = ""
    if len(message) > MAX_MESSAGE_LENGTH:
        # If text is too long for one message, split it up over several
        for block in [message[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(message), MAX_MESSAGE_LENGTH)]:
            send(block, group_id)
            time.sleep(0.3)
        data["text"] = ""
    else:
        data["text"] = message
    if image is not None:
        data["picture_url"] = image
    # Prevent sending message if there's no content
    # It would be rejected anyway
    if data["text"] or data.get("picture_url"):
        response = requests.post("https://api.groupme.com/v3/bots/post", data=data)


# Core routing
@app.route("/")
@cache.cached(timeout=CACHE_TIMEOUT)
def home():
    return render_template("index.html", static_commands=static_commands.keys(), commands=[(key, commands[key].DESCRIPTION) for key in commands])


# Module interfaces
@app.route("/memes")
@cache.cached(timeout=CACHE_TIMEOUT)
def memes():
    return render_template("memes.html",
                           memes=zip(commands["meme"].templates.keys(),
                                     [len(commands["meme"].templates[template]) - 1 for template in commands["meme"].templates]))


@app.route("/analytics/<group_id>")
def analytics(group_id):
    # TODO: clear up users/leaderboards naming
    users = commands["analytics"].leaderboards.get(group_id)
    return render_template("analytics.html", users=users)


# Local testing
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?")
    args = parser.parse_args()
    if args.command:
        print(process_message(Message(text=args.command)))
    else:
        while True:
            print(process_message(Message(text=input("> "))))
