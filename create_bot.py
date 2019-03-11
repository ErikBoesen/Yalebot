import requests
import os
import json
from pick import pick

token = os.environ["GROUPME_ACCESS_TOKEN"]

def read(prop, default):
    return input(f"{prop} [{default}]: ") or default

groups = requests.get(f"https://api.groupme.com/v3/groups?token={token}").json()["response"]
bot = {
    "name": read("name", "Yalebot"),
    "group_id": pick([groups[group_id]["name"] for group_id in groups])[0]
    "avatar_url": read("Avatar URL", "https://i.groupme.com/310x310.jpeg.1c88aac983ff4587b15ef69c2649a09c"),
    "callback_url": read("Callback URL", "https://yalebot.herokuapp.com/"),
    "dm_notification": True,
}
result = requests.post(f"https://api.groupme.com/v3/bots?token={token}").json()
with open("groups.json", "r+") as f:
    groups = json.load(f)
    groups[result["group_id"]] = {
        "name": bot["name"],
        "bot_id": result["bot_id"],
    }
    json.dump(groups, f)
