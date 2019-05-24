from .base import Module
import json
import random


class Player:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
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
        self.selection = []
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
        # Filter out Pick 2 cards for now
        self.black = [card for card in self.black if card.count("_") == 1]
        self.black = [card.replace("_", "_" * 5) for card in self.black]
        random.shuffle(self.black)

    def build_white_deck(self):
        with open("resources/cah/white.json", "r") as f:
            self.white = json.load(f)
        random.shuffle(self.white)

    def choose_black_card(self):
        self.current_black_card = self.black.pop()

    def assign_czar(self, user_id=None):
        if user_id is None:
            user_id = random.choice(list(self.players.keys()))
        # TODO: Do we need this function?
        # At least make it more pythonic
        self.czar_user_id = user_id

    def join(self, user_id, name):
        if user_id in self.players:
            return False
        self.players[user_id] = Player(user_id, name)
        self.deal(user_id)
        if self.czar_user_id is None:
            self.assign_czar(user_id)

    def deal(self, user_id):
        for i in range(self.hand_size):
            self.players[user_id].pick_up_white(self.white.pop())

    def has_played(self, user_id):
        """
        Check whether a user has played a card already this round.
        """
        for candidate_id, card in self.selection:
            if candidate_id == user_id:
                return True
        return False

    def player_choose(self, user_id, card_index):
        if self.has_played(user_id):
            return False
        card = self.players[user_id].hand.pop(card_index)
        self.selection.append((user_id, card))
        # TODO: this is repeated from above, make a method to draw cards
        self.players[user_id].pick_up_white(self.white.pop())
        return True

    def players_needed(self):
        return len(self.players) - len(self.selection) - 1

    def is_czar(self, user_id):
        return self.czar_user_id == user_id

    def get_nth_card_user_id(self, n):
        # TODO: this relies on dictionaries staying in a static order, which they do NOT necessarily!
        # Use a less lazy implementation.
        counter = 0
        for user_id, card in self.selection:
            if counter == card_index:
                return user_id, card
            counter += 1

    def czar_choose(self, card_index):
        user_id, card = get_nth_card_user_id(card_index)
        self.players[user_id].score(self.current_black_card)
        self.choose_black_card()
        self.selection = []
        self.assign_czar(user_id)
        # Return card and winner
        return card, self.players[user_id]

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

    def add_player(self, user_id, name):
        self.playing[user_id] = group_id
        self.games[group_id].join(user_id, name)

    def response(self, query, message):
        # TODO: fix this mess
        arguments = query.split()
        command = arguments.pop(0)
        group_id = message.group_id
        user_id = message.user_id
        name = message.name
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
            for user_id in game.players:
                self.playing.pop(user_id)
            return "Game ended. Say !cah start to start a new game."
        elif command == "join":
            if user_id in self.playing:
                return "You're already in a game."
            if group_id not in self.games:
                return "No game in progress. Say !cah start to start a game."
            self.add_player(user_id, name)
            return f"{name} has joined the game! Please go to https://yalebot.herokuapp.com/cah/join to play."
        elif command == "leave":
            if user_id in self.playing:
                self.playing.pop(user_id)
                return f"Removed {name} from the game."
            else:
                return f"{name} is not currently in a game."
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
