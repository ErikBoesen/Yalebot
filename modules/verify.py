from .base import Module
import random
import json
import random
import requests
import os


class Verify(Module):
    DESCRIPTION = "Check if users are actually Yale admits"
    ARGC = 0
    POSITIVE_EMOJI = "✅"
    NEGATIVE_EMOJI = "❓"

    def __init__(self):
        super().__init__()
        with open("resources/admit_names.json") as f:
            self.admits = json.load(f)

    def get_members(self, group_id):
        response = requests.get(f"https://api.groupme.com/v3/groups/{group_id}?token={self.ACCESS_TOKEN}").json()
        members = response["response"]["members"]
        return [member["name"] for member in members]

    def response(self, query, message):
        if not query:
            members = self.get_members(message["group_id"])
            return "\n".join([self.check_member(member) for member in members])
        return self.check_user(query.strip("@"))

    def is_admit(self, name: str):
        """
        Check calculated list of admits to determine if user is part of Yale '23.
        """
        return (name.lower() in self.admits)

    def check_member(self, name: str):
        """
        Get a SHORT report on whether a user is verified.
        """
        verified = self.is_admit(name)
        icon = self.emojus(verified)
        return f"{icon} {name}"

    def emojus(self, verified: bool):
        return self.POSITIVE_EMOJI if verified else self.NEGATIVE_EMOJI

    def check_user(self, name: str):
        """
        Get a LONG report on whether a user is verified.
        """
        name = name.strip()
        if name.lower() == "yalebot":
            return "Y'all think you're smart, don't you?"
        verified = self.is_admit(name)
        icon = self.emojus(verified)
        status = "is" if verified else "isn't"
        return f"{icon} {name} {status} listed on the Yale 2023 Admits website."


class McCarthy(Verify):
    DESCRIPTION = "Vet Stalinist spies in our homeland"
    ARGC = 0
    POSITIVE_EMOJI = "🇺🇸"
    NEGATIVE_EMOJI = "☭"

    def response(self, query, message):
        return self.check_user(random.choice(self.get_members(message["group_id"])))
