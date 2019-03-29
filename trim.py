import os
from groupy.client import Client

GROUP_ID = 46649296
TOKEN = os.environ["GROUPME_ACCESS_TOKEN"]
client = Client.from_token(TOKEN)

group = client.groups.get(id=GROUP_ID)

with open("extraneous_users.txt", "r") as f:
    targets = f.readlines()
targets = [target.strip("\n") for target in targets]

for member in group.members:
    if member.name in targets:
        print(member.remove())
