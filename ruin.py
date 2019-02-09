import os
from groupy.client import Client
import binascii

GROUP_ID = 47859426
TOKEN = os.environ['GROUPME_ACCESS_TOKEN']
client = Client.from_token(TOKEN)

def random():
    return binascii.b2a_hex(os.urandom(15))

group = client.groups.get(id=GROUP_ID)
group.update(name=random())

for _ in range(100):
    group.post(text=random())

for member in group.members:
    member.update(nickname=random())
    member.remove()
