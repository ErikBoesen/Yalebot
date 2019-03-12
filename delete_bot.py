import requests
import json
from pick import pick
import os

token = os.environ["GROUPME_ACCESS_TOKEN"]

with open("groups.json", "r") as f:
    groups = json.load(f)
group_name = pick([groups[group_id]["name"] for group_id in groups])[0]
# Knowing name chosen, get group ID
for candidate in groups:
    if groups[candidate]["name"] == group_name:
        group_id = candidate
        break
print(f"Leaving group {group_id}/{group_name}.")
request = requests.post(f"https://api.groupme.com/v3/bots/destroy?token={token}", data={"bot_id": groups[group_id]["bot_id"]})
if request.ok:
    print("Success.")
    with open("groups.json", "w") as f:
        del groups[group_id]
        json.dump(groups, f)
else:
    print("Failure: ", end="")
    print(request.json())
