from .base import Module
import json

class Vet(Module):
    DESCRIPTION = "Check if users are actually Yale admits"
    def __init__(self):
        super().__init__()
        with open('resources/admit_names.json') as f:
            self.admits = json.load(f)

    def response(self, query, message):
        return self.check_user(query.strip('@'))

    def is_admit(self, name: str):
        """
        Check calculated list of admits to determine if user is part of Yale '23.
        """
        return (name in self.admits)

    def check_user(self, name: str):
        """
        Get a string-formatted report on whether a user is verified.
        """
        if name.lower() == "yalebot":
            return "Y'all think you're smart, don't you?"
        return "{name} {status} a verified admit according to the Yale 2023 Admits website.".format(name=name,
                                                                                                    status="is" if self.is_admit(name) else "is NOT")

