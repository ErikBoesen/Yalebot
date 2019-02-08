#from .base import Module
import requests
import re
import sys
from pprint import pprint
import os

# The initial code this is based on was taken from https://github.com/octohub/GroupMeAnalytics
# All credit goes to the author of that program.

at = os.environ["GROUPME_ACCESS_TOKEN"]
GROUP = 46649296

class Analytics:
    def __init__(self):
        groups_data = self.get_group_data()
        self.prepare_analysis_of_group(groups_data, GROUP)

    def get_group_data(self):
        response = requests.get('https://api.groupme.com/v3/groups?token='+at)
        data = response.json()

        if len(data['response']) == 0:
            print("You are not part of any groups.")
            return
        for i in range(len(data['response'])):
            group = data['response'][i]['name']
            print(str(i)+"\'"+group+"\'")
        return data

    def prepare_analysis_of_group(self, groups_data, GROUP):
        # these three lines simply display info to the user before the analysis begins
        number_of_messages = self.get_number_of_messages_in_group(groups_data, GROUP)
        print("Analyzing "+str(number_of_messages) + " messages from " + group_name)

        #these two lines put all the members currently in the group into a dictionary
        members_of_group_data = self.get_group_members(groups_data, GROUP)
        user_dictionary = self.prepare_user_dictionary(members_of_group_data)

        #this line calls the "analyze_group" method which goes through the entire conversation
        user_id_mapped_to_user_data = self.analyze_group(GROUP, user_dictionary, number_of_messages)

        #this line displays the data to the user
        self.display_data(user_id_mapped_to_user_data)

    def get_number_of_messages_in_group(self, groups_data, GROUP):
        i = 0
        while True:
            if GROUP == groups_data['response'][i]['group_id']:
                return groups_data['response'][i]['messages']['count']
            i += 1

    def get_group_members(self, groups_data, GROUP):
        i = 0
        while True:
            if GROUP == groups_data['response'][i]['group_id']:
                return groups_data['response'][i]['members']
            i += 1

    def prepare_user_dictionary(self, members_of_group_data):
        user_dictionary = {}
        i = 0
        while True:
            try:
                user_id = members_of_group_data[i]['user_id']
                nickname = members_of_group_data[i]['nickname']
                user_dictionary[user_id] = [nickname, 0.0, 0.0, 0.0, 0.0, {}, {}, 0.0]
                # [0] = nickname, [1] = total messages sent in group, like count, [2] = likes per message,
                # [3] = average likes received per message, [4] = total words sent, [5] = dictionary of likes received from each member
                # [6] = dictionary of shared likes, [7] = total likes given

            except IndexError:  # it will reach here when it gets to the end of the members
                return user_dictionary
            i += 1
        return user_dictionary


    def analyze_group(self, GROUP, user_id_mapped_to_user_data, number_of_messages):

        response = requests.get('https://api.groupme.com/v3/groups/'+GROUP+'/messages?token='+at)
        data = response.json()
        message_with_only_alphanumeric_characters = ''
        message_id = 0
        iterations = 0.0
        while True:
            for i in range(20):  # in range of 20 because API sends 20 messages at once
                try:

                    iterations += 1
                    name = data['response']['messages'][i]['name']  # grabs name of sender
                    message = data['response']['messages'][i]['text']  # grabs text of message
                    #print(message)
                    try:
                        #  strips out special characters
                        message_with_only_alphanumeric_characters = re.sub(r'\W+', ' ', str(message))
                    except ValueError:
                        pass  # this is here to catch errors when there are special characters in the message e.g. emoticons
                    sender_id = data['response']['messages'][i]['sender_id']  # grabs sender id
                    list_of_favs = data['response']['messages'][i]['favorited_by']  # grabs list of who favorited message
                    length_of_favs = len(list_of_favs)  # grabs number of users who liked message


                    #grabs the number of words in message
                    number_of_words_in_message = len(re.findall(r'\w+', str(message_with_only_alphanumeric_characters)))

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
                    user_id_mapped_to_user_data[sender_id][4] += number_of_words_in_message

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
                    message_id = data['response']['messages'][i]['id']
                    remaining = iterations/number_of_messages
                    remaining *= 100
                    remaining = round(remaining, 2)
                    print(str(remaining)+' percent done')

            payload = {'before_id': message_id}
            response = requests.get('https://api.groupme.com/v3/groups/'+GROUP+'/messages?token='+at, params=payload)
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
