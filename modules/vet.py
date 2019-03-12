from .base import Module
import random
import json
import requests
import os

token = os.environ["GROUPME_ACCESS_TOKEN"]

class Vet(Module):
    DESCRIPTION = "Check if users are actually Yale admits"
    ARGC = 0
    POSITIVE_EMOJI = "😁"
    NEGATIVE_EMOJI = "🌧"
    def __init__(self):
        super().__init__()
        with open('resources/admit_names.json') as f:
            self.admits = json.load(f)

    def get_members(self, group_id):
        response = requests.get("https://api.groupme.com/v3/groups/%s?token=%s" % (group_id, token)).json()
        members = response["response"]["members"]
        return [member["name"] for member in members]

    def response(self, query, message):
        if not query:
            members = self.get_members(message["group_id"])
            return "\n".join([self.check_member(member) for member in members])
        return self.check_user(query.strip('@'))

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
        icon = random.choice(self.POSITIVE_EMOJI if verified else self.NEGATIVE_EMOJI)
        return f"{icon} {name}"

    def check_user(self, name: str):
        """
        Get a LONG string-formatted report on whether a user is verified.
        """
        name = name.strip()
        if name.lower() == "yalebot":
            return "Y'all think you're smart, don't you?"
        verified = self.is_admit(name)
        icon = random.choice(self.POSITIVE_EMOJI if verified else self.NEGATIVE_EMOJI)
        status = "is" if verified else "is NOT"
        return f"{icon} {name} {status} a verified admit according to the Yale 2023 Admits website."
