import os
import requests
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from threading import Thread
import discord
import asyncio
from pymessenger.bot import Bot as FacebookBot
import re
import modules
import difflib

from utils import Message, SenderType


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)

MAX_MESSAGE_LENGTH = 1000
PREFIX = "!"

static_commands = {
    "ping": "Pong!",
    "testing": "Join the Yalebot testing server: https://groupme.com/join_group/49940116/f2x20kxx",
    "add": "Add me to your own group here: https://yalebot.herokuapp.com",

    "sam": "❗❗❗N O 💪 F L E X 💪 Z O N E ❗❗❗",
    "social": "https://docs.google.com/spreadsheets/d/10m_0glWVUncKCxERsNf6uOJhfeYU96mOK0KvgNURIBk/edit?fbclid=IwAR35OaPO6czQxZv26A6DEgEH-Qef0kCSe4nXxl8wcIfDml-BfLx4ksVtp6Y#gid=0",
    "meetup": ("", "https://i.groupme.com/750x1200.jpeg.b0ca5f6e660a4356be2925222e6f8246.large"),
    "test": "https://erikboesen.com/yalepuritytest",
    "dislike": "👎😬👎\n 🦵🦵",
    "shrug": r"¯\_(ツ)_/¯",
    "oh": ("", "https://i.groupme.com/766x750.jpeg.9209520c57e848369444ca498e31f90a.large"),
    "jah": ("", "https://i.groupme.com/766x750.jpeg.3eb07fe422db4b81947b634a1b309d48.large"),
    "bulldog": "Bulldog!  Bulldog!\nBow, wow, wow\nEli Yale\nBulldog!  Bulldog!\nBow, wow, wow\nOur team can never fail\n\nWhen the sons of Eli\nBreak through the line\nThat is the sign we hail\nBulldog!  Bulldog!\nBow, wow, wow\nEli Yale!",
    "popcorn": "https://www.youtube.com/watch?v=9nwOm4AAXwc",
    "yyle": "https://www.youtube.com/watch?v=SsZDxL-YMYc",
    "discord": "If you must: https://discord.gg/5EScef4",
    "bang": ("", "https://i.groupme.com/720x1440.png.c76127a21867451093edd11bbb09d75d.large"),
    "chike": ("", "https://i.groupme.com/1021x1400.jpeg.70192657c76745ab809357d0512d4951.large"),
    "pressed": ("", "https://i.groupme.com/540x719.jpeg.2229bdb9f15247a7a112ac0be95e065a.large"),
    "flex": "👮🏽🚨🚔 PULL OVER 👮🏽🚨🚔\n\n😤Put your hands behind your back😤\n\n🗣I'm taking you into custody🗣\n\n📝And registering you as a📝\n\n🔥😩FLEX OFFENDER😩🔥",
    "amma": ("", "https://i.groupme.com/714x456.jpeg.66fb9e9dacab4cd9b860b084eceff282.large"),
    "ohno": ("", "https://i.groupme.com/1280x720.jpeg.f7c11a529a3b4a7195f71fa6be5ebfef.large"),
    "defuse": ("", "https://i.groupme.com/500x500.jpeg.26cbc006bcbf47048ade8a896b1e3d5a.large"),
}

commands = {
    "about": modules.About(),
    "countdown": modules.Countdown(),
    "verify": modules.Verify(),
    "yalenews": modules.YaleNews(),
    "record": modules.Record(),
    "groups": modules.Groups(),
    "weather": modules.Weather(),

    "conversationstarter": modules.ConversationStarter(),
    "funfact": modules.FunFact(),
    "lyrics": modules.Lyrics(),
    "nasa": modules.NASA(),
    "sad": modules.Sad(),
    "xkcd": modules.XKCD(),
    "elizabeth": modules.Elizabeth(),
    "dania": modules.Dania(),
    "jake": modules.Jake(),
    "carlos": modules.Carlos(),
    "crista": modules.Crista(),
    "maria": modules.Maria(),
    "annie": modules.Annie(),
    "chat": modules.Chat(),
    "kelly": modules.Kelly(),
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
    "amber": modules.Amber(),
    "uwu": modules.UWU(),
    "quote": modules.Quote(),
    "dog": modules.Dog(),
    "funny": modules.Funny(),
    "kelbo": modules.Kelbo(),
    "boink": modules.Boink(),
    "conversationstarter": modules.ConversationStarter(),
    "funfact": modules.FunFact(),
    "ship": modules.Ship(),
    "hema": modules.Hema(),
    "victor": modules.Victor(),
    "truman": modules.Truman(),
    "nato": modules.NATO(),
    "tiya": modules.Tiya(),
    "crist": modules.Crist(),
    "power": modules.Power(),
    "cah": modules.CardsAgainstHumanity(),
    "colleges": modules.Colleges(),
    "tictactoe": modules.TicTacToe(),
    "zalgo": modules.Zalgo(),
    "flip": modules.Flip(),
    "mccarthy": modules.McCarthy(),
    "circle": modules.Circle(),
    "jpeg": modules.JPEG(),
}
system_responses = {
    "welcome": modules.Welcome(),
    "mourn": modules.Mourn(),
}


class Response(db.Model):
    __tablename__ = "responses"
    name = db.Column(db.String(64), primary_key=True)
    content = db.Column(db.String(256))
    image_url = db.Column(db.String(128))

    def __init__(self, name, content, image_url):
        self.name = name
        self.content = content
        self.image_url = image_url


def process_message(message):
    responses = []
    forename = message.name.split(" ", 1)[0]
    f_matches = re.search("can i get an? (.+) in the chat", message.text, flags=re.IGNORECASE | re.MULTILINE)
    if f_matches is not None and len(f_matches.groups()):
        responses.append(f_matches.groups()[0] + " ❤")
    if message.sender_type != SenderType.BOT:
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
                if len(list(filter(None, query.split("\n")))) < commands[command].ARGC:
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
                    elif query in meme_commands:
                        responses.append(PREFIX + query + ": meme command; provide captions separated by newlines.")
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
                    response = Response(new_command, content, message.image_url)
                    db.session.add(response)
                    db.session.commit()
                    responses.append(f"Command {new_command} registered successfully.")
                elif not content and not message.image_url:
                    db.session.delete(response)
                    db.session.commit()
                    responses.append(f"Command {new_command} unregistered.")
                else:
                    responses.append(f"Command {new_command} already registered!")
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
        for option in system_responses:
            if system_responses[option].RE.match(message.text):
                responses.append(system_responses[option].response(message.text, message))
        """
        if system_responses["welcome"].RE.match(text):
            check_names = system_responses["welcome"].get_names(text)
            for check_name in check_names:
                send(commands["vet"].check_user(check_name), group_id)
        """
    return responses


def reply(message, group_id):
    send(process_message(Message.from_groupme(message)), group_id)


@app.route("/", methods=["POST"])
def groupme_webhook():
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
        data["text"] = ""
    else:
        data["text"] = message
    if image is not None:
        data["picture_url"] = image
    # Prevent sending message if there's no content
    # It would be rejected anyway
    if data["text"] or data.get("picture_url"):
        response = requests.post("https://api.groupme.com/v3/bots/post", data=data)


@app.route("/")
def home():
    return render_template("index.html", static_commands=static_commands.keys(), commands=[(key, commands[key].DESCRIPTION) for key in commands])


@app.route("/memes")
def memes():
    return render_template("memes.html",
                           memes=zip(commands["meme"].templates.keys(),
                                     [len(commands["meme"].templates[template]) - 1 for template in commands["meme"].templates]))


@app.route("/analytics/<group_id>")
def analytics(group_id):
    # TODO: clear up users/leaderboards naming
    users = commands["analytics"].leaderboards[group_id]
    return render_template("analytics.html", users=users)


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


@app.route("/cah", methods=["GET"])
def cah():
    access_token = request.args["access_token"]
    user = requests.get(f"https://api.groupme.com/v3/users/me?token={access_token}").json()["response"]
    user_id = user["user_id"]
    game = commands["cah"].get_user_game(user_id)
    if game is None:
        return "You're not in a game yet, say !cah join"
    player = game.players[user_id]
    is_czar = game.is_czar(user_id)

    cards = list(game.selection.values()) if is_czar else player.hand
    return render_template("cah.html",
                           is_czar=is_czar,
                           black_card=game.current_black_card,
                           cards=cards,
                           score=len(player.won))


@app.route("/cah", methods=["POST"])
def cah_entry():
    data = request.get_json()
    access_token = data["access_token"]
    user = requests.get(f"https://api.groupme.com/v3/users/me?token={access_token}").json()["response"]
    user_id = user["user_id"]
    game = commands["cah"].get_user_game(user_id)
    player = game.players[user_id]
    group_id = game.group_id
    if game.is_czar(user_id):
        send("The Card Czar has selected ", group_id)
    else:
        game.player_choose(user_id, data["card_index"])
    return "ok", 200


if __name__ == "__main__":
    while True:
        print(process_message(Message({}, input("> "), name="Tester", group_id=49940116)))


discord_client = discord.Client()


async def start():
    await discord_client.start(os.environ.get("DISCORD_TOKEN"))


def run_loop(loop):
    loop.run_forever()


@discord_client.event
async def on_ready():
    """Run when the bot is ready."""
    print(f"Logged into Discord as {discord_client.user.name} (ID {discord_client.user.id}).")
    await discord_client.change_presence(status=discord.Status.online, activity=discord.Game(name="GitHub: ErikBoesen/Yalebot!"))


@discord_client.event
async def on_message(message):
    """Catch a user's messages and figure out what to return."""
    # Log message
    response = process_message(Message.from_discord(message))
    await discord_send(response, message.channel)


async def discord_send(content, channel):
    if isinstance(content, list):
        for item in content:
            await discord_send(item, channel)
    elif isinstance(content, tuple):
        content, image = content
        await discord_send(content, channel)
        await discord_send(image, channel)
    elif content:
        await channel.send(content)


@discord_client.event
async def on_member_join(self, member):
    """
    When a member joins a server.
    :param member: The name of the member who joined.
    """
    await discord_send("**Welcome " + member.mention + " to the server!** :rocket:", member.server.default_channel)


@discord_client.event
async def on_member_remove(self, member):
    """
    When a member has left or been kicked from a server.
    :param member: The name of the member who left.
    """
    await discord_send(member.mention + " has left the server. :frowning:", member.server.default_channel)


asyncio.get_child_watcher()
loop = asyncio.get_event_loop()
loop.create_task(start())

thread = Thread(target=run_loop, args=(loop,))
thread.start()


# Facebook Messenger section
facebook_bot = FacebookBot(os.environ["FACEBOOK_ACCESS_TOKEN"])


def facebook_reply(recipient_id, message):
    response = process_message(Message.from_facebook(message))
    facebook_send(recipient_id, response)


@app.route("/facebook", methods=["GET", "POST"])
def receive_message():
    if request.method == "GET":
        """
        Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.
        """
        token_sent = request.args.get("hub.verify_token")
        if token_sent == os.environ.get("FACEBOOK_VERIFY_TOKEN"):
            return request.args.get("hub.challenge")
        return "Invalid verification token."
    # get whatever message a user sent the bot
    output = request.get_json()
    for event in output["entry"]:
        messaging = event["messaging"]
        for message in messaging:
            if message.get("message"):
                # Get Messenger ID for user so we know where to send response back to
                recipient_id = message["sender"]["id"]
                if message["message"].get("text"):
                    Thread(target=facebook_reply, args=(recipient_id, message)).start()
    return "ok", 200


def facebook_send(recipient_id, content):
    if isinstance(content, list):
        for item in content:
            facebook_send(recipient_id, item)
    elif isinstance(content, tuple):
        content, image = content
        facebook_send(recipient_id, content)
        facebook_bot.send_image_url(recipient_id, image)
    elif content:
        facebook_bot.send_text_message(recipient_id, content)
