# Flask
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

# Other
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

MAX_MESSAGE_LENGTH = 1000
PREFIX = "!"
CACHE_TIMEOUT = 60 * 60


# Database models
class Bot(db.Model):
    __tablename__ = "bots"
    group_id = db.Column(db.String(16), unique=True, primary_key=True)
    group_name = db.Column(db.String(50))
    bot_id = db.Column(db.String(26), unique=True)
    owner_id = db.Column(db.String(16))
    owner_name = db.Column(db.String(64))
    access_token = db.Column(db.String(32))


class Response(db.Model):
    __tablename__ = "responses"
    name = db.Column(db.String(64), primary_key=True)
    content = db.Column(db.String(256))
    image_url = db.Column(db.String(128))


# Management console
@app.route("/manager", methods=["GET", "POST"])
def manager():
    access_token = request.args.get("access_token")
    if request.method == "POST":
        # Build and send bot data
        group_id = request.form["group_id"]
        bot = {
            "name": request.form["name"] or "Yalebot",
            "group_id": group_id,
            "avatar_url": request.form["avatar_url"] or "https://i.groupme.com/310x310.jpeg.1c88aac983ff4587b15ef69c2649a09c",
            "callback_url": "https://yalebot.herokuapp.com/",
            "dm_notification": False,
        }
        me = requests.get(f"https://api.groupme.com/v3/users/me?token={access_token}").json()["response"]
        result = requests.post(f"https://api.groupme.com/v3/bots?token={access_token}",
                               json={"bot": bot}).json()["response"]["bot"]
        group = requests.get(f"https://api.groupme.com/v3/groups/{group_id}?token={access_token}").json()["response"]

        # Store in database
        registrant = Bot(group_id, group["name"], result["bot_id"], me["user_id"], me["name"], access_token)
        db.session.add(registrant)
        db.session.commit()
    if access_token is None:
        return redirect("https://oauth.groupme.com/oauth/authorize?client_id=46tkWF26m1juUxxvRGKUjVqVjbejYK4Njz3VA4ZZjWhr5dtH", code=302)
    groups = requests.get(f"https://api.groupme.com/v3/groups?token={access_token}").json()["response"]
    bots = requests.get(f"https://api.groupme.com/v3/bots?token={access_token}").json()["response"]
    if os.environ.get("DATABASE_URL") is not None:
        groups = [group for group in groups if not Bot.query.get(group["group_id"])]
        bots = [bot for bot in bots if Bot.query.get(bot["group_id"])]
    # TEMPORARY; fill in information that used to not be collected
    if bots:
        for bot in bots:
            # TODO remove this abomination
            group_id = bot["group_id"]
            this_bot = Bot.query.get(group_id)
            me = requests.get(f"https://api.groupme.com/v3/users/me?token={access_token}").json()["response"]
            group = requests.get(f"https://api.groupme.com/v3/groups/{group_id}?token={access_token}").json()["response"]
            this_bot.group_name = group["name"]
            this_bot.access_token = access_token
            this_bot.owner_name = me["name"]
        db.session.commit()
    return render_template("manager.html", access_token=access_token, groups=groups, bots=bots)


@app.route("/delete", methods=["POST"])
def delete_bot():
    data = request.get_json()
    access_token = data["access_token"]
    bot = Bot.query.get(data["group_id"])
    req = requests.post(f"https://api.groupme.com/v3/bots/destroy?token={access_token}", json={"bot_id": bot.bot_id})
    if req.ok:
        db.session.delete(bot)
        db.session.commit()
        return "ok", 200


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
                        response = Response(new_command, content, message.image_url)
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
            elif command == "stats":
                count = Bot.query.count()
                responses.append(f"I am currently in {count} GroupMe groups. Add me to more at https://yalebot.herokuapp.com!")
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
        if "thank" in message.text.lower() and "yalebot" in message.text.lower():
            responses.append("You're welcome, " + forename + "! :)")
    if message.sender_type == SenderType.SYSTEM:
        for option in system_commands:
            if system_commands[option].RE.match(message.text):
                responses.append(system_commands[option].response(message.text, message))
        if system_commands["welcome"].RE.match(message.text):
            check_names = system_commands["welcome"].get_names_groupme(message.text)
            for check_name in check_names:
                responses.append(commands["verify"].check_user(check_name))
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
    this_bot = Bot.query.get(group_id)
    # Close session so it won't remain locked on database
    db.session.close()
    data = {
        "bot_id": this_bot.bot_id,
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
