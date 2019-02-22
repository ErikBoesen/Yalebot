import os
from groupy.client import Client

GROUP_ID = 46649296
TOKEN = os.environ['GROUPME_ACCESS_TOKEN']
client = Client.from_token(TOKEN)

group = client.groups.get(id=GROUP_ID)

targets = ['Chike Iwuagwu', 'hiba hamid', 'AIDAN YOO(NOT SIMON)', 'Walli Chen (penn daddy)', 'Simon', 'Nick Bausenwein (Penn)', 'Eashan Sahai', 'AJ Manning', 'Margaret LaMarche', 'Rachel Wilson', 'Nitin S', 'Mia McDonald', 'David Yang', 'David Lu', 'serin b', 'Halsey Ziglar', 'Langston Luck', 'Sophie Hirt', 'Nick Bausenwein (Penn)', 'Jacob K', 'Nicole Overton']

for member in group.members:
    if member.nickname in targets:
        print(member.remove())
