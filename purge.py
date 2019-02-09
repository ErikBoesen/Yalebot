import requests
import os

GROUP_ID = 46649296
TOKEN = os.environ['GROUPME_ACCESS_TOKEN']

def get_members(group_id):
    response = requests.get('https://api.groupme.com/v3/groups/%d?token=%s' % (group_id, TOKEN))
    return response.json()['response']['members']

def kick(group_id, target_id):
    response = requests.get('https://api.groupme.com/v3/groups/%d/members/%s/remove?token=%s' % (group_id, TOKEN, target_id))

targets = ['Chike Iwuagwu', 'hiba hamid', 'AIDAN YOO(NOT SIMON)', 'Walli Chen (penn daddy)', 'Simon', 'Nick Bausenwein (Penn)', 'Eashan Sahai', 'AJ Manning', 'Margaret LaMarche', 'Rachel Wilson', 'Nitin S', 'Mia McDonald', 'David Yang', 'David Lu', 'serin b', 'Halsey Ziglar', 'Langston Luck', 'Sophie Hirt']

for member in get_members(GROUP_ID):
    if member['nickname'] in targets:
        kick(GROUP_ID, member['id'])

