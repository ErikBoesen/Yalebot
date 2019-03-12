import requests
import os
import json
from pick import pick

token = os.environ["GROUPME_ACCESS_TOKEN"]

def read(prop, default):
    return input(f"{prop} [{default}]: ") or default

groups = requests.get(f"https://api.groupme.com/v3/groups?token={token}").json()["response"]
group_name = pick([group["name"] for group in groups])[0]
# Knowing name chosen, get group ID
for candidate in groups:
    if candidate["name"] == group_name:
        group_id = candidate["group_id"]
        break
print(f"Selected group {group_id}/{group_name}.")

bot = {
    "name": read("name", "Yalebot"),
    "group_id": group_id,
    "avatar_url": read("Avatar URL", "https://i.groupme.com/310x310.jpeg.1c88aac983ff4587b15ef69c2649a09c"),
    "callback_url": read("Callback URL", "https://yalebot.herokuapp.com/"),
    "dm_notification": False,
}
result = requests.post(f"https://api.groupme.com/v3/bots?token={token}",
                       json={"bot": bot}).json()["response"]

with open("groups.json", "r+") as f:
    groups = json.load(f)
    groups[result["group_id"]] = {
        "name": bot["name"],
        "bot_id": result["bot_id"],
    }
    json.dump(groups, f)
