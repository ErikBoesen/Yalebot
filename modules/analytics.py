#from .base import Module
import requests
import re
import sys
from pprint import pprint
import os

at = os.environ["GROUPME_ACCESS_TOKEN"]
GROUP_ID = 46649296

class Analytics:
    DESCRIPTION = "View statistics on user activity in the chat"

    users = {}
    def __init__(self):
        self.generate_data()

    def generate_data(self):
        self.users = {}
        group = self.get_group(GROUP_ID)

        # Display info to user before the analysis begins
        message_count = group["messages"]["count"]
        print("Analyzing " + str(message_count) + " messages.")

        # Make dictionary of members
        self.populate_users(group["members"])

        # Perform analysis
        self.analyze_group(GROUP_ID, message_count)
        return "%d messages processed."

    def get_group(self, group_id):
        response = requests.get("https://api.groupme.com/v3/groups/%d?token=%s" % (group_id, at))
        data = response.json()
        return data["response"]

    def new_user(self, name):
        return {"name": name, "messages": 0, "likes": 0, "likes_received": 0.0}

    def populate_users(self, members):
        for member in members:
            self.users[member["user_id"]] = self.new_user(member["name"])

    def analyze_group(self, group_id, message_count):
        message_id = 0
        message_number = 0
        while message_number < message_count:
            params = {
                # Get maximum number of messages at a time
                "limit": 100,
            }
            if message_id:
                params["before_id"] = message_id
            response = requests.get("https://api.groupme.com/v3/groups/%d/messages?token=%s" % (group_id, at), params=params)
            messages = response.json()["response"]["messages"]
            for message in messages:
                message_number += 1
                name = message["name"]

                sender_id = message["sender_id"]
                likers = message["favorited_by"]

                if sender_id not in self.users.keys():
                    self.users[sender_id] = self.new_user(name)

                # Fill the name in if user liked a message but hasn"t yet been added to the dictionary
                if not self.users[sender_id].get("name"):
                    self.users[sender_id]["name"] = name

                for liker_id in likers:
                    if liker_id not in self.users.keys():
                        # Leave name blank until user sends their first message
                        self.users[liker_id] = self.new_user("")
                    self.users[liker_id]["likes"] += 1

                self.users[sender_id]["messages"] += 1  # Increment sent message count
                self.users[sender_id]["likes_received"] += len(likers)

            message_id = messages[-1]["id"]  # Get last message"s ID for next request
            remaining = 100 *  message_number / message_count
            print("\r%.2f%% done" % remaining, end="")

    def response(self, query):
        parameters = query.split(" ")
        command = parameters.pop(0)
        output = ""
        if command == "regenerate":
            return self.generate_data()
        if command == "profile":
            return "Profiling coming soon"
        elif command == "leaderboard":
            users = [self.users[key] for key in self.users]
            users.sort(key=lambda user: user["messages"], reverse=True)
            leaders = users[:10]
            for place, user in enumerate(leaders):
                output += str(place + 1) + ". " + user["name"] + " / Messages Sent: %d" % user["messages"]
                output += " / Likes Given: %d" % user["likes"]
                output += " / Likes Received: %d" % user["likes_received"]
                output += "\n"
        return output

if __name__ == "__main__":
    print(Analytics().response("leaderboard"))
