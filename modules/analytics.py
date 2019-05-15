from .base import Module
import requests
import re
import sys
from pprint import pprint
import os


class Analytics(Module):
    DESCRIPTION = "View statistics on user activity in the chat"
    groups = {}
    leaderboards = {}

    def generate_data(self, group_id):
        self.groups[group_id] = {}
        group = self.get_group(group_id)

        # Display info to user before the analysis begins
        message_count = group["messages"]["count"]
        print("Analyzing " + str(message_count) + " messages.")

        # Make dictionary of members
        self.populate_users(group["members"], group_id)

        # Perform analysis
        self.analyze_group(group_id, message_count)

        # Make ordered list
        # TODO: clear up users/leaderboards naming
        users = [self.groups[group_id][key] for key in self.groups[group_id]]
        users.sort(key=lambda user: user["Messages"], reverse=True)
        self.leaderboards[group_id] = users
        return f"{message_count} messages processed. View statistics at https://yalebot.herokuapp.com/analytics/{group_id}, or use `!analytics leaderboard` to view a list of the top users!"

    def get_group(self, group_id):
        return requests.get(f"https://api.groupme.com/v3/groups/{group_id}?token={self.ACCESS_TOKEN}").json()["response"]

    def new_user(self, name):
        return {"Name": name, "Messages": 0, "Likes": 0, "Likes Received": 0, "Likes Received Per Message": 0}

    def populate_users(self, members, group_id):
        for member in members:
            self.groups[group_id][member["user_id"]] = self.new_user(member["name"])

    def analyze_group(self, group_id, message_count):
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

                if sender_id not in self.groups[group_id].keys():
                    self.groups[group_id][sender_id] = self.new_user(name)

                # Fill the name in if user liked a message but hasn"t yet been added to the dictionary
                if not self.groups[group_id][sender_id].get("Name"):
                    self.groups[group_id][sender_id]["Name"] = name

                for liker_id in likers:
                    if liker_id not in self.groups[group_id].keys():
                        # Leave name blank until user sends their first message
                        self.groups[group_id][liker_id] = self.new_user("")
                    self.groups[group_id][liker_id]["Likes"] += 1

                self.groups[group_id][sender_id]["Messages"] += 1  # Increment sent message count
                self.groups[group_id][sender_id]["Likes Received"] += len(likers)

            try:
                message_id = messages.pop()["id"]  # Get last message's ID for next request
            except Exception:
                # If history has been cleared
                break
            percentage = int(10 * message_number / message_count) * 10
            if percentage > last_percentage:
                last_percentage = percentage
                print("%d%% done" % percentage)
        for user_id in self.groups[group_id]:
            if self.groups[group_id][user_id]["Messages"] > 0:
                self.groups[group_id][user_id]["Likes Received Per Message"] = (self.groups[group_id][user_id]["Likes Received"] / self.groups[group_id][user_id]["Messages"])

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
