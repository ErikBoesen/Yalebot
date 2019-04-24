from .base import Module
import json
import random


REDIRECT_URL = "https://oauth.groupme.com/oauth/authorize?client_id=iEs9DrSihBnH0JbOGZSWK8SdsqRt0pUn8EpulL8Fia3rf6QM"


class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.hand = []
        self.won = []

    def pick_up_white(self, card):
        self.hand.append(card)

    def score(self, card):
        self.won.append(card)

    """
    def discard_all(self):
        hand = self.hand
        self.hand = None
        return hand
    """


class Game:
    def __init__(self, group_id):
        self.group_id = group_id
        self.players = {}
        self.hand_size = 8
        self.build_decks()

    def build_decks(self):
        self.build_black_deck()
        self.build_white_deck()

    def build_black_deck(self):
        with open("resources/cah/black.json", "r") as f:
            self.black = json.load(f)
        random.shuffle(self.black)

    def build_white_deck(self):
        with open("resources/cah/white.json", "r") as f:
            self.white = json.load(f)
        random.shuffle(self.white)

    def join(self, user_id):
        if user_id in self.players:
            return False
        self.players[user_id] = Player(user_id)
        self.deal(user_id)

    def deal(self, user_id):
        for i in range(self.hand_size):
            self.players[user_id].pick_up(self.white.pop())

    """
    def discard(self, user_id):
        if user_id not in self.players:
            return False
        self.white = self.players[user_id].discard_all() + self.white
        self.deal(user_id)
    """


class CardsAgainstHumanity(Module):
    DESCRIPTION = "Play everyone's favorite card game for terrible people. Commands: start, end"
    ARGC = 1
    games = {}
    # TODO: use references to Player objects??
    playing = {}

    def response(self, query, message):
        # TODO: fix this mess
        arguments = query.split()
        command = arguments.pop(0)
        group_id = message["group_id"]
        user_id = message["user_id"]
        name = message["name"]
        if command == "start":
            if group_id in self.games:
                return "Game already started!"
            self.games[group_id] = Game(group_id)
            return (f"Cards Against Humanity game started in group #{group_id}.\n"
                    "Run !cah end to terminate the game.\n"
                    "To join the game and choose your cards, go to https://yalebot.herokuapp.com/cah")
        elif command == "end":
            if group_id not in self.games:
                return "No game in progress."
            game = self.games.pop(group_id)
            # TODO: free players, etc. Otherwise they're stuck
            for player in game.players:
                self.playing.pop(player.user_id)
            return "Game ended. Run !cah start to start a new game."
        elif command == "join":
            if user_id in self.playing:
                return "You're already in a game."
            if group_id not in self.games:
                # TODO: debug
                return "No game in progress. Games: " + str(self.games)
            self.playing[user_id] = group_id
            self.games[group_id].join(user_id)
            return f"{name} has joined the game! Please go to {REDIRECT_URL} to play."
        elif command == "info":
            return f"{len(self.games)} games in progress: " + ", ".join(self.games.keys())
        """
        elif command == "refresh":
            self.games[group_id].refresh(user_id)
        """
