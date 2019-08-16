from .base import Module
import requests
import re
import sys
from pprint import pprint
import datetime
import os


class Group:
    users = {}
    leaderboard = {}
    frequency = {}

    def __init__(self, group_id):
        raw = requests.get(f"https://api.groupme.com/v3/groups/{group_id}?token={self.ACCESS_TOKEN}").json()["response"]
        # Display info to user before the analysis begins
        self.message_count = raw["messages"]["count"]
        print("Analyzing " + str(self.message_count) + " messages.")

        # Make dictionary of members
        self.populate_users(raw["members"], group_id)

        # Pull message data and parse through it
        self.analyze_group()

        # Create leaderboard list
        self.build_leaderboard()

    def populate_users(self, members):
        for member in members:
            self.users[member["user_id"]] = self.new_user(member["name"])

    def new_user(self, name):
        return {"Name": name, "Messages": 0, "Likes": 0, "Likes Received": 0, "Likes Received Per Message": 0}

    def analyze_group(self):
        message_id = 0
        message_number = 0
        last_percentage = 0
        while message_number < message_count:
            params = {
                # Get maximum number of messages at a time
                "limit": 100,
            }
            if message_id:
                params["before_id"] = message_id
            response = requests.get(f"https://api.groupme.com/v3/groups/{group_id}/messages?token={self.ACCESS_TOKEN}", params=params)
            messages = response.json()["response"]["messages"]
            for message in messages:
                message_number += 1
                name = message["name"]

                sender_id = message["sender_id"]
                likers = message["favorited_by"]

                if sender_id not in self.users.keys():
                    self.users[sender_id] = self.new_user(name)

                # Fill the name in if user liked a message but hasn't yet been added to the dictionary
                if not self.users[sender_id].get("Name"):
                    self.users[sender_id]["Name"] = name

                for liker_id in likers:
                    if liker_id not in self.users.keys():
                        # Leave name blank until user sends their first message
                        self.users[liker_id] = self.new_user("")
                    self.users[liker_id]["Likes"] += 1

                self.users[sender_id]["Messages"] += 1  # Increment sent message count
                self.users[sender_id]["Likes Received"] += len(likers)

                # Counting over time
                date = datetime.date.fromtimestamp(message["created_at"])
                if self.frequency.get(date):
                    self.frequency[date] += 1
                else:
                    self.frequency[date] = 1
            try:
                message_id = messages.pop()["id"]  # Get last message's ID for next request
            except Exception:
                # If history has been cleared
                break
            percentage = int(10 * message_number / message_count) * 10
            if percentage > last_percentage:
                last_percentage = percentage
                print("%d%% done" % percentage)
        # Consolidate all of own messages into one user
        yalebot = self.new_user("Yalebot")
        yalebot_id = None
        duplicate_ids = []
        # TODO: this should definitely not rely solely on name...
        for user_id in self.users:
            if self.users[user_id]["Name"] == "Yalebot":
                yalebot_id = user_id
                for field in self.users[user_id]:
                    if type(yalebot[field]) != str:
                        yalebot[field] += self.users[user_id][field]
        if yalebot_id:
            self.users[yalebot_id] = yalebot
            for user_id in duplicate_ids:
                self.users.pop(user_id)
        # Iterate through users and calculate averages
        for user_id in self.users:
            if self.users[user_id]["Messages"] > 0:
                self.users[user_id]["Likes Received Per Message"] = (self.users[user_id]["Likes Received"] / self.users[user_id]["Messages"])

    def build_leaderboard():
        """
        Make descending ordered list of users by number of messages sent.
        """
        users = list(self.users.values())
        users.sort(key=lambda user: user["Messages"], reverse=True)
        self.leaderboard = users


class Analytics(Module):
    DESCRIPTION = "View statistics on user activity in the chat"
    groups = {}

    def generate_data(self, group_id):
        self.groups[group_id] = Group(group_id)

        return f"{message_count} messages processed. View statistics at https://yalebot.herokuapp.com/analytics/{group_id}, or use `!analytics leaderboard` to view a list of the top users!"

    def response(self, query, message):
        parameters = query.split(" ")
        command = parameters.pop(0)
        output = ""
        if command == "generate":
            return self.generate_data(message.group_id)
        elif command == "leaderboard":
            try:
                length = int(parameters.pop(0))
            except Exception:
                length = 10
            leaders = self.leaderboards[message.group_id][:length]
            for place, user in enumerate(leaders):
                output += str(place + 1) + ". " + user["Name"] + " / Messages Sent: %d" % user["Messages"]
                output += " / Likes Given: %d" % user["Likes"]
                output += " / Likes Received: %d" % user["Likes Received"]
                output += "\n"
        else:
            return "Please state a valid command!"
        return output
