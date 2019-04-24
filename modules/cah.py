from .base import Module
import json
import random


class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.hand = []

    def pick_up(self, card):
        self.hand.append(card)


class Game:
    def __init__(self, group_id):
        self.group_id = group_id
        self.players = {}
        with open("resources/cah/black.json", "r") as f:
            self.black = json.load(f)
        with open("resources/cah/white.json", "r") as f:
            self.white = json.load(f)
        random.shuffle(self.black)
        random.shuffle(self.white)
        self.hand_size = 8

    def join(self, user_id):
        if user_id in self.players:
            return False
        else:
            player = Player(user_id)
            for i in self.hand_size:
                player.
            self.players[user_id] = player


class CardsAgainstHumanity(Module):
    DESCRIPTION = "Play everyone's favorite card game for terrible people. Commands: start, end"
    games = {}

    def response(self, query, message):
        command, query = query.split(None, 1)
        group_id = message["group_id"]
        if command == "start":
            if group_id in self.games:
                return "Game already started!"
            else:
                self.games[group_id] = Game(group_id)
                return (f"Cards Against Humanity game started in group #{group_id}.\n"
                        "Run !cah end to terminate the game.\n"
                        "To join the game and choose your cards, go to https://yalebot.herokuapp.com/cah")
        elif command == "end":
            if group_id in self.games:
                self.games.pop(group_id)
                return "Game ended. Run !cah start to start a new game."
            else:
                return "No game in progress."

        # TODO: allow discarding whole hand
