import modules
import os
import re
import requests
import json
import difflib
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)

MAX_MESSAGE_LENGTH = 1000
PREFIX = "!"

static_commands = {
    "ping": "Pong!",
    "testing": "Join the Yalebot testing server: https://groupme.com/join_group/49940116/f2x20kxx",

    "sam": "❗❗❗N O 💪 F L E X 💪 Z O N E ❗❗❗",
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
    "discord": "If you must: https://discord.gg/5EScef4",
    "bang": ("", "https://i.groupme.com/720x1440.png.c76127a21867451093edd11bbb09d75d.large"),
    "oof": ("Oh?", "https://i.groupme.com/1500x1125.jpeg.9b2c341aa9854831ab2525d7e21e974a.large"),
    "tease": ("", "https://i.groupme.com/936x1246.jpeg.d0d60970b329415cac1d7a1825a783a7.large"),
    "chike": ("", "https://i.groupme.com/1021x1400.jpeg.70192657c76745ab809357d0512d4951.large"),
    "pressed": ("", "https://i.groupme.com/540x719.jpeg.2229bdb9f15247a7a112ac0be95e065a.large"),
    "alex": ("", "https://i.groupme.com/1021x1400.jpeg.7bd963eae3824435bf749b96ce4fd84a.large"),
    "bddschedule": "https://bulldogdays2019.sched.com/",
    "flex": "👮🏽🚨🚔 PULL OVER 👮🏽🚨🚔\n\n😤Put your hands behind your back😤\n\n🗣I'm taking you into custody🗣\n\n📝And registering you as a📝\n\n🔥😩FLEX OFFENDER😩🔥",
    "amma": ("", "https://i.groupme.com/714x456.jpeg.66fb9e9dacab4cd9b860b084eceff282.large"),
    "ohno": ("", "https://i.groupme.com/1280x720.jpeg.f7c11a529a3b4a7195f71fa6be5ebfef.large"),
    "bddalbum": "https://photos.app.goo.gl/YyFXCQHnY1KWoznY7",
    "add": "Add me to your own group here: https://yalebot.herokuapp.com",
    "jah": ("", "https://i.groupme.com/766x750.jpeg.3eb07fe422db4b81947b634a1b309d48.large"),
    "defuse": ("", "https://i.groupme.com/500x500.jpeg.26cbc006bcbf47048ade8a896b1e3d5a.large"),
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
    "renee": modules.Renee(),
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
    "boink": modules.Boink(),
    "ship": modules.Ship(),
    "hema": modules.Hema(),
    "victor": modules.Victor(),
    "truman": modules.Truman(),
    "nato": modules.NATO(),
    "tiya": modules.Tiya(),
    "crist": modules.Crist(),
}
system_responses = {
    "welcome": modules.Welcome(),
    "mourn": modules.Mourn(),
}

F_PATTERN = re.compile("can i get an? (.+) in the chat", flags=re.IGNORECASE | re.MULTILINE)


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
    f_matches = F_PATTERN.search(text)
    if f_matches is not None and len(f_matches.groups()):
        reply(f_matches.groups()[0] + " ❤", group_id)
    if message["sender_type"] != "bot":
        if text.startswith(PREFIX):
            instructions = text[len(PREFIX):].strip().split(None, 1)
            command = instructions.pop(0).lower()
            query = instructions[0] if len(instructions) > 0 else ""
            # Prevent response to long string of exclamation marks
            if PREFIX in command and set(command) == set(PREFIX):
                pass
            # Check if there's a static response for this command
            elif command in static_commands:
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

        if "thank" in text.lower() and "yalebot" in text.lower():
            reply("You're welcome, " + forename + "! :)", group_id)
    if message["system"]:
        for option in system_responses:
            if system_responses[option].RE.match(text):
                reply(system_responses[option].response(text, message), group_id)
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
    this_bot = Bot.query.get(group_id)
    data = {
        "bot_id": this_bot.bot_id,
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


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


def in_group(group_id):
    return db.session.query(db.exists().where(Bot.group_id == group_id)).scalar()


@app.route("/manager", methods=["GET", "POST"])
def manager():
    access_token = request.args["access_token"]
    if request.method == "POST":
        # Build and send bot data
        bot = {
            "name": request.form["name"] or "Yalebot",
            "group_id": request.form["group_id"],
            "avatar_url": request.form["avatar_url"] or "https://i.groupme.com/310x310.jpeg.1c88aac983ff4587b15ef69c2649a09c",
            "callback_url": "https://yalebot.herokuapp.com/",
            "dm_notification": False,
        }
        me = requests.get(f"https://api.groupme.com/v3/users/me?token={access_token}").json()["response"]
        result = requests.post(f"https://api.groupme.com/v3/bots?token={access_token}",
                               json={"bot": bot}).json()["response"]["bot"]

        # Store in database
        registrant = Bot(result["group_id"], result["bot_id"], me["user_id"])
        db.session.add(registrant)
        db.session.commit()
    groups = requests.get(f"https://api.groupme.com/v3/groups?token={access_token}").json()["response"]
    bots = requests.get(f"https://api.groupme.com/v3/bots?token={access_token}").json()["response"]
    if os.environ.get("DATABASE_URL") is not None:
        groups = [group for group in groups if not Bot.query.get(group["group_id"])]
        bots = [bot for bot in bots if Bot.query.get(bot["group_id"])]
    return render_template("manager.html", access_token=access_token, groups=groups, bots=bots)


class Bot(db.Model):
    __tablename__ = "bots"
    # TODO: store owner also
    group_id = db.Column(db.String(16), unique=True, primary_key=True)
    bot_id = db.Column(db.String(26), unique=True)
    owner_id = db.Column(db.String(16))

    def __init__(self, group_id, bot_id, owner_id):
        self.group_id = group_id
        self.bot_id = bot_id
        self.owner_id = owner_id


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
