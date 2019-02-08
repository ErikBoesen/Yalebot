#from .base import Module
import requests
import re
import sys
from pprint import pprint
import os

# The initial code this is based on was taken from https://github.com/octohub/GroupMeAnalytics
# All credit goes to the author of that program.

at = os.environ["GROUPME_ACCESS_TOKEN"]
GROUP_ID = 46649296

class Analytics:
    users = []
    def __init__(self):
        group = self.get_group(GROUP_ID)
        self.prepare_analysis_of_group(group)

    def get_group_data(self, group_id):
        response = requests.get('https://api.groupme.com/v3/groups?token=' + at)
        data = response.json()
        return data['response']

    def prepare_analysis_of_group(self, group):
        # these three lines simply display info to the user before the analysis begins
        message_count = group['messages']['count']
        print("Analyzing " + str(message_count) + " messages.")

        # Make dictionary of members
        self.populate_users(group['members'])

        # This line calls the "analyze_group" method which goes through the entire conversation
        self.users = self.analyze_group(GROUP_ID, user_dictionary, message_count)

        #this line displays the data to the user
        self.display_data(self.users)

    def new_user(self, name):
        return {"name": name, "messages": 0, "likes": 0, "average_likes_per_message": 0.0, "average_likes_received": 0.0}

    def populate_users(self, members):
        for member in members:
            user_id = member['user_id']
            name = member['name']  # TODO: May need to be nickname not name
            user_dictionary[user_id] = self.new_user(nickname)
            # TODO: This is a terrible system and will be removed once it no longer needs to be referenced.
            # [0] = nickname, [1] = total messages sent in group, like count, [2] = likes per message,
            # [3] = average likes received per message, [4] = total words sent, [5] = dictionary of likes received from each member
            # [6] = dictionary of shared likes, [7] = total likes given

    def analyze_group(self, GROUP_ID, self.users, message_count):
        message_id = 0
        message_number = 0
        while True:
            response = requests.get('https://api.groupme.com/v3/groups/' + GROUP_ID + '/messages?token=' + at)
            messages = response.json()['response']['messages']
            for i in range(20):  # API sends 20 messages at once
                message_number += 1
                name = messages[i]['name']
                message = messages[i]['text']

                sender_id = messages[i]['sender_id']
                likers = messages[i]['favorited_by']
                likers_count = len(likers)

                if sender_id not in self.users.keys():
                    self.users[sender_id] = self.new_user(name)

                # Fill the name in if user liked a message but hasn't yet been added to the dictionary
                if self.users[sender_id]['name'] == '':
                    self.users[sender_id]['name'] = name

                for liker_id in likers:
                    if liker_id not in self.users.keys():
                        # Leave name blank until user sends their first message
                        self.users[user_id] = self.new_user('')
                    self.users[liker_id]["likes"] += 1

                self.users[sender_id][1] += 1  # add one to sent message count
                self.users[sender_id][2] += likers_count

            message_id = messages[19]['id']  # Get last message's ID for next request
            remaining = message_number / message_count
            remaining *= 100
            remaining = round(remaining, 2)
            print(str(remaining)+' percent done')

            payload = {'before_id': message_id}
            response = requests.get('https://api.groupme.com/v3/groups/'+GROUP_ID+'/messages?token='+at, params=payload)
            data = response.json()

    def display_data(self, self.users):
        for key in self.users:
            print(self.users[key][0] + ' Data:')
            print('Messages Sent: ' + str(self.users[key][1]))
            print('Total Likes Given: ' + str(self.users[key][7]))
            try:
                print('Self Likes: ' + str(self.users[key][5][key]))
                self_likes = self.users[key][5][key]
            except KeyError:
                self_likes = 0
                print('Self Likes: ' + str(0))
            print('Total Likes Received: ' + str(self.users[key][2]))
            print('Average Likes Received Per Message: ' + str(self.users[key][3]))

            print('Total Likes Received with Self Likes Subtracted: ' +
                  str(self.users[key][2] - self_likes))

            total_likes_minus_self_likes = self.users[key][2] - self_likes
            try:
                new_avg = total_likes_minus_self_likes / self.users[key][1]
            except ZeroDivisionError:  # for the case where the user has sent 0 messages
                new_avg = 0
            print('Average Likes Received Per Message with Self Likes Subtracted: '
                  + str(new_avg))

            print('Total Words Sent: ' + str(self.users[key][4]))

            print('Likes Received from each member and also what percent of the total likes received is from said member :')
            for key_inner in self.users[key][5]:
                percent = (self.users[key][5][key_inner] / self.users[key][2]) * 100
                percent = round(percent, 2)
                sys.stdout.write(self.users[key_inner][0])  # Name of liker
                sys.stdout.write(' : ' + str(self.users[key][5][key_inner]) + ', ') # number of likes to user
                sys.stdout.write(str(percent) + '%, ')
            print

            print('Percent of each member\'s total likes that went to ' + str(self.users[key][0]) + ': ')
            for key_inner in self.users[key][5]:
                sys.stdout.write(self.users[key_inner][0])
                convert_to_percent = (self.users[key][5][key_inner] /
                                      self.users[key_inner][7]) * 100
                convert_to_percent = round(convert_to_percent, 2)
                sys.stdout.write(': ' + str(convert_to_percent) + '%, ')
            print

            test = self.users[key][6]
            print('Number of times you liked the same post as another member and what percent of the posts you '
                  'liked were liked by that same member: ')
            for key_inner in self.users[key][6]:
                percent_shared = (self.users[key][6][key_inner]/self.users[key][7])*100
                percent_shared = round(percent_shared, 2)
                sys.stdout.write(self.users[key_inner][0])
                sys.stdout.write(': ' + str(self.users[key][6][key_inner]) + ', ')
                sys.stdout.write(str(percent_shared)+'%, ')
            print
            print

if __name__ == "__main__":
    print(Analytics().response(""))
