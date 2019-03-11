import requests
import os
import json
from pick import pick

with open("groups.json", "r") as f:
    groups = json.load(f)
group_name = pick([groups[group_id]["name"] for group_id in groups])[0]
# Knowing name chosen, get group ID
for candidate in groups:
    if groups[candidate]["name"] == group_name:
        group_id = candidate
print(group_id)

text = input("Message: ")
requests.post("https://api.groupme.com/v3/bots/post", data={"text": text, "bot_id": groups[group_id]["bot_id"]})
