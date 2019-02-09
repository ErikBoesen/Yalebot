import requests
import os

GROUP_ID = 46649296
TOKEN = os.environ['GROUPME_ACCESS_TOKEN']

def members(group_id):
    response = requests.get('https://api.groupme.com/v3/groups/%d?token=%s' % (group_id, TOKEN))
    return response.json()['response']['members']

targets = ['Chike Iwuagwu', 'hiba hamid', 'AIDAN YOO(NOT SIMON)', 'Walli Chen (penn daddy)', 'Simon', 'Nick Bausenwein (Penn)', 'Eashan Sahai', 'AJ Manning', 'Margaret LaMarche', 'Rachel Wilson', 'Nitin S', 'Mia McDonald', 'David Yang', 'David Lu', 'serin b', 'Halsey Ziglar', 'Langston Luck', 'Sophie Hirt']
target_ids = []

for member in members(GROUP_ID):
    if member['nickname'] in targets:
        target_ids.append(member['id'])

