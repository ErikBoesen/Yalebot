#from .base import Module


class Game():#Module):
    def __init__(self):
        self.started = False

    def response(self, query, name):
        """
        Handle general game starting, cancelling, etc. logic.
        """
        pass


class TicTacToe(Game):
    RES = 3
    def __init__(self):
        super().__init__()

    def value_to_char(self, value: int):
        # TODO: Better name
        if value is None:
            return "_"
        else:
            return ("X", "O")[value]

    def render_board(self):
        # TODO: This function is actual garbage even if it's working garbage
        board_template = "%c | %c | %c\n--+---+--\n%c | %c | %c\n--+---+--\n%c | %c | %c"
        board_items = [item for sublist in self.board for item in sublist]
        board_items = [self.value_to_char(item) for item in board_items]
        print(board_template % tuple(board_items))

    def start_game(self, players):
        self.started = True
        self.board = [[None] * self.RES] * self.RES
        self.render_board()
        self.turn = 0
        self.players = players
        return "Tic-Tac-Toe game started between {player1} & {player2}! It is {player1}'s turn (X) first.".format(player1=players[0],
                                                                                                                  player2=players[1])

    def cancel_game(self):
        self.started = False
        self.board = None
        self.players = []
        return "Tic-Tac-Toe game cancelled."

    def turn(self):
        pass

    def response(self, query, name):
        #super().response(query)
        parameters = query.split(" ")
        if parameters[0] == "start":
            if self.started:
                return "A game is already in progress!"
            else:
                return self.start_game(players=[name, " ".join(parameters[1:])[1:]])
        elif parameters[0] == "cancel":
            if self.started:
                return self.cancel_game()
            else:
                return "No game is in progress."
        else:
            return "Invalid command."

if __name__ == "__main__":
    ttt = TicTacToe()
    while True:
        print(ttt.response(input("> "), 'Erik Bøsen'))

