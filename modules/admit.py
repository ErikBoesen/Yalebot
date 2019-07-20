from .base import Module
import json


class Admit(Module):
    DESCRIPTION = "Look up an admitted student's question responses"
    ARGC = 1

    def __init__(self):
        super().__init__()
        with open("resources/admits.json", "r") as f:
            self.admits = json.load(f)

    def response(self, query, message):
        student = self.admits.get(query.lower())
        if student is None:
            return "Couldn't find a student named '" + query + "'."
        return self.bullet_list([(q.strip(":"), a) for q, a in student.items()])
