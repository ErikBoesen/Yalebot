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
        self.selection = {}
        self.hand_size = 8
        self.build_decks()
        self.czar_user_id = None
        self.choose_black_card()

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

    def choose_black_card(self):
        self.current_black_card = self.black.pop()

    def assign_czar(self, user_id=None):
        # TODO: Do we need this function?
        # At least make it more pythonic
        self.czar_user_id = user_id

    def join(self, user_id):
        if user_id in self.players:
            return False
        self.players[user_id] = Player(user_id)
        self.deal(user_id)
        if self.czar_user_id is None:
            self.assign_czar(user_id)

    def deal(self, user_id):
        for i in range(self.hand_size):
            self.players[user_id].pick_up_white(self.white.pop())

    def player_choose(self, user_id, card_index):
        # TODO: check if user has already picked a card
        card = self.players[user_id].hand.pop(card_index)
        self.selection[card_index] = card

    def is_czar(self, user_id):
        return self.czar_user_id == user_id

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

    def __init__(self):
        super().__init__()
        self.games = {}
        # TODO: use references to Player objects??
        self.playing = {}

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
                    "Say !cah join to join, or !cah end to terminate the game.\n")
        elif command == "end":
            if group_id not in self.games:
                return "No game in progress."
            game = self.games.pop(group_id)
            for player in game.players:
                self.playing.pop(player.user_id)
            return "Game ended. Say !cah start to start a new game."
        elif command == "join":
            if user_id in self.playing:
                return "You're already in a game."
            if group_id not in self.games:
                return "No game in progress. Say !cah start to start a game."
            self.playing[user_id] = group_id
            self.games[group_id].join(user_id)
            return f"{name} has joined the game! Please go to {REDIRECT_URL} to play."
        elif command == "info":
            return str(self.games) + " " + str(self.playing) + " " + str(self)
        """
        elif command == "refresh":
            self.games[group_id].refresh(user_id)
        """

    def get_user_game(self, user_id):
        game_group_id = self.playing.get(user_id)
        if game_group_id is None:
            return None
        return self.games[game_group_id]
