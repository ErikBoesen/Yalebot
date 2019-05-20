import os
from groupy.client import Client

GROUP_ID = 46649296
TOKEN = os.environ['GROUPME_ACCESS_TOKEN']
client = Client.from_token(TOKEN)

group = client.groups.get(id=GROUP_ID)

with open("purge.txt", "r") as f:
    targets = [name.strip() for name in f.readlines()]
print(targets)

for member in group.members:
    if member.nickname in targets:
        print(member.remove())
