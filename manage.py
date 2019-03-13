import requests
import os
import json
from pick import pick
import argparse

parser = argparse.ArgumentParser(description="Control Yalebot directly")
parser.add_argument("verb")
parser.add_argument("--token", default=os.environ["GROUPME_ACCESS_TOKEN"])
args = parser.parse_args()

def read(prop, default):
    return input(f"{prop} [{default}]: ") or default

if args.verb == "create_bot":
    groups = requests.get(f"https://api.groupme.com/v3/groups?token={args.token}").json()["response"]
    group_name = pick([group["name"] for group in groups])[0]
    # Knowing name chosen, get group id
    for candidate in groups:
        if candidate["name"] == group_name:
            group_id = candidate["group_id"]
            break
    print(f"Selected group {group_id}/{group_name}.")

    bot = {
        "name": read("name", "yalebot"),
        "group_id": group_id,
        "avatar_url": read("avatar url", "https://i.groupme.com/310x310.jpeg.1c88aac983ff4587b15ef69c2649a09c"),
        "callback_url": read("callback url", "https://yalebot.herokuapp.com/"),
        "dm_notification": false,
    }
    result = requests.post(f"https://api.groupme.com/v3/bots?token={args.token}",
                           json={"bot": bot}).json()["response"]["bot"]

    with open("groups.json", "r+") as f:
        groups = json.load(f)
        groups[result["group_id"]] = {
            "name": bot["name"],
            "bot_id": result["bot_id"],
        }
        json.dump(groups, f)

elif args.verb == "destroy_bot":
    with open("groups.json", "r") as f:
        groups = json.load(f)
    group_name = pick([groups[group_id]["name"] for group_id in groups])[0]
    # Knowing name chosen, get group ID
    for candidate in groups:
        if groups[candidate]["name"] == group_name:
            group_id = candidate
            break
    print(f"Leaving group {group_id}/{group_name}.")
    request = requests.post(f"https://api.groupme.com/v3/bots/destroy?token={args.token}", data={"bot_id": groups[group_id]["bot_id"]})
    if request.ok:
        print("Success.")
        with open("groups.json", "w") as f:
            del groups[group_id]
            json.dump(groups, f)
    else:
        print("Failure: ", end="")
        print(request.json())
elif args.verb == "send":
    with open("groups.json", "r") as f:
        groups = json.load(f)
    group_name = pick([groups[group_id]["name"] for group_id in groups])[0]
    # Knowing name chosen, get group ID
    for candidate in groups:
        if groups[candidate]["name"] == group_name:
            group_id = candidate
            break
    print(f"Selected group {group_id}/{group_name}.")

    text = input("Message: ")
    requests.post("https://api.groupme.com/v3/bots/post", data={"text": text, "bot_id": groups[group_id]["bot_id"]})
