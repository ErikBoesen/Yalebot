import os
import requests
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import argparse
from threading import Thread
import discord
import asyncio
from pymessenger.bot import Bot as FacebookBot

from utils import Message
from processing import PREFIX, static_commands, commands, process_message


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)

MAX_MESSAGE_LENGTH = 1000


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
    if isinstance(message, tuple):
        text, image = message
    else:
        text = message
        image = None
    if len(text) > MAX_MESSAGE_LENGTH:
        # If text is too long for one message, split it up over several
        for block in [text[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]:
            send(block, group_id)
        data["text"] = ""
    else:
        data["text"] = text
    if image is not None:
        data["picture_url"] = image
    # Prevent sending message if there's no content
    # It would be rejected anyway
    if data["text"] or data["picture_url"]:
        response = requests.post("https://api.groupme.com/v3/bots/post", data=data)


@app.route("/")
def home():
    return render_template("index.html", static_commands=static_commands.keys(), commands=[(key, commands[key].DESCRIPTION) for key in commands])


@app.route("/memes")
def memes():
    return render_template("memes.html",
                           memes=zip(commands["meme"].templates.keys(),
                                     [len(commands["meme"].templates[template]) - 1 for template in commands["meme"].templates]))


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
    parser = argparse.ArgumentParser(description="Testing interface to Yalebot.")
    parser.add_argument("message")
    args = parser.parse_args()
    print(process_message(Message({}, args.message, name="Tester")))


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


# TODO: reimplement join/leave listeners

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
                    print(message)
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
