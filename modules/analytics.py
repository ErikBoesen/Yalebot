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
        user_id_mapped_to_user_data = self.analyze_group(GROUP_ID, user_dictionary, message_count)

        #this line displays the data to the user
        self.display_data(user_id_mapped_to_user_data)

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

    def analyze_group(self, GROUP_ID, user_id_mapped_to_user_data, message_count):
        message_id = 0
        iterations = 0.0
        while True:
            response = requests.get('https://api.groupme.com/v3/groups/'+GROUP_ID+'/messages?token='+at)
            messages = response.json()['response']['messages']
            for i in range(20):  # API sends 20 messages at once
                try:
                    iterations += 1
                    name = messages[i]['name']
                    message = messages[i]['text']

                    sender_id = messages[i]['sender_id']
                    list_of_favs = messages[i]['favorited_by']
                    length_of_favs = len(list_of_favs)


                    if sender_id not in user_id_mapped_to_user_data.keys():
                        user_id_mapped_to_user_data[sender_id] = [name, 0.0, 0.0, 0.0, 0.0, {}, {}, 0.0]

                    #this if statement is here to fill the name in for the case where a user id liked a message but had
                    #yet been added to the dictionary
                    if user_id_mapped_to_user_data[sender_id][0] == '':
                        user_id_mapped_to_user_data[sender_id][0] = name

                    for user_id in list_of_favs:
                        if user_id in user_id_mapped_to_user_data[sender_id][5].keys():
                            user_id_mapped_to_user_data[sender_id][5][user_id] += 1
                        else:
                            user_id_mapped_to_user_data[sender_id][5][user_id] = 1

                    for user_id in list_of_favs:
                        for user_id_inner in list_of_favs:
                            if user_id not in user_id_mapped_to_user_data.keys():
                                # leave name blank because this means a user is has liked a message but has yet to be added
                                # to the dictionary. So leave the name blank until they send their first message.
                                user_id_mapped_to_user_data[user_id] = ['', 0.0, 0.0, 0.0, 0.0, {}, {}, 0.0]
                            if user_id == user_id_inner:
                                user_id_mapped_to_user_data[user_id][7] += 1
                                continue  # pass because you don't want to count yourself as sharing likes with yourself
                            try:
                                user_id_mapped_to_user_data[user_id][6][user_id_inner] += 1
                            except KeyError:
                                user_id_mapped_to_user_data[user_id][6][user_id_inner] = 1

                    user_id_mapped_to_user_data[sender_id][1] += 1  # add one to sent message count
                    user_id_mapped_to_user_data[sender_id][2] += length_of_favs

                except IndexError:
                    print("COMPLETE")
                    print
                    for key in user_id_mapped_to_user_data:
                        try:
                            user_id_mapped_to_user_data[key][3] = user_id_mapped_to_user_data[key][2] / user_id_mapped_to_user_data[key][1]
                        except ZeroDivisionError:  # for the case where the user has sent 0 messages
                            user_id_mapped_to_user_data[key][3] = 0
                    return user_id_mapped_to_user_data

            if i == 19:
                    message_id = messages[i]['id']
                    remaining = iterations/message_count
                    remaining *= 100
                    remaining = round(remaining, 2)
                    print(str(remaining)+' percent done')

            payload = {'before_id': message_id}
            response = requests.get('https://api.groupme.com/v3/groups/'+GROUP_ID+'/messages?token='+at, params=payload)
            data = response.json()

    def display_data(self, user_id_mapped_to_user_data):
        for key in user_id_mapped_to_user_data:
            print(user_id_mapped_to_user_data[key][0] + ' Data:')
            print('Messages Sent: ' + str(user_id_mapped_to_user_data[key][1]))
            print('Total Likes Given: ' + str(user_id_mapped_to_user_data[key][7]))
            try:
                print('Self Likes: ' + str(user_id_mapped_to_user_data[key][5][key]))
                self_likes = user_id_mapped_to_user_data[key][5][key]
            except KeyError:
                self_likes = 0
                print('Self Likes: ' + str(0))
            print('Total Likes Received: ' + str(user_id_mapped_to_user_data[key][2]))
            print('Average Likes Received Per Message: ' + str(user_id_mapped_to_user_data[key][3]))

            print('Total Likes Received with Self Likes Subtracted: ' +
                  str(user_id_mapped_to_user_data[key][2] - self_likes))

            total_likes_minus_self_likes = user_id_mapped_to_user_data[key][2] - self_likes
            try:
                new_avg = total_likes_minus_self_likes / user_id_mapped_to_user_data[key][1]
            except ZeroDivisionError:  # for the case where the user has sent 0 messages
                new_avg = 0
            print('Average Likes Received Per Message with Self Likes Subtracted: '
                  + str(new_avg))

            print('Total Words Sent: ' + str(user_id_mapped_to_user_data[key][4]))

            print('Likes Received from each member and also what percent of the total likes received is from said member :')
            for key_inner in user_id_mapped_to_user_data[key][5]:
                percent = (user_id_mapped_to_user_data[key][5][key_inner] / user_id_mapped_to_user_data[key][2]) * 100
                percent = round(percent, 2)
                sys.stdout.write(user_id_mapped_to_user_data[key_inner][0])  # Name of liker
                sys.stdout.write(' : ' + str(user_id_mapped_to_user_data[key][5][key_inner]) + ', ') # number of likes to user
                sys.stdout.write(str(percent) + '%, ')
            print

            print('Percent of each member\'s total likes that went to ' + str(user_id_mapped_to_user_data[key][0]) + ': ')
            for key_inner in user_id_mapped_to_user_data[key][5]:
                sys.stdout.write(user_id_mapped_to_user_data[key_inner][0])
                convert_to_percent = (user_id_mapped_to_user_data[key][5][key_inner] /
                                      user_id_mapped_to_user_data[key_inner][7]) * 100
                convert_to_percent = round(convert_to_percent, 2)
                sys.stdout.write(': ' + str(convert_to_percent) + '%, ')
            print

            test = user_id_mapped_to_user_data[key][6]
            print('Number of times you liked the same post as another member and what percent of the posts you '
                  'liked were liked by that same member: ')
            for key_inner in user_id_mapped_to_user_data[key][6]:
                percent_shared = (user_id_mapped_to_user_data[key][6][key_inner]/user_id_mapped_to_user_data[key][7])*100
                percent_shared = round(percent_shared, 2)
                sys.stdout.write(user_id_mapped_to_user_data[key_inner][0])
                sys.stdout.write(': ' + str(user_id_mapped_to_user_data[key][6][key_inner]) + ', ')
                sys.stdout.write(str(percent_shared)+'%, ')
            print
            print

if __name__ == "__main__":
    print(Analytics().response(""))
