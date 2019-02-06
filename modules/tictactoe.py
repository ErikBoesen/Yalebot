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
        string = ""
        for y in range(self.RES):
            for x in range(self.RES):
                string += self.value_to_char(self.board[y][x])
            string += "\n"
        return string

    def start_game(self, players):
        self.started = True
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.render_board()
        self.turn = 0
        self.players = players
        return "Tic-Tac-Toe game started between {player1} & {player2}! It is {player1}'s turn (X) first.\n{board}".format(player1=players[0],
                                                                                                                           player2=players[1],
                                                                                                                           board=self.render_board())
    def end_game(self):
        self.started = False
        self.board = None
        self.players = []

    def cancel_game(self):
        self.end_game()
        return "Tic-Tac-Toe game cancelled."

    def place(self, x, y):
        self.board[y][x] = self.turn
        if self.check_win():
            self.end_game()
            return self.render_board() + "\n" + self.players[self.turn] + " wins!"
        self.turn = (1, 0)[self.turn]
        return self.render_board() + "\n" + ("It is now %s's turn" % self.players[self.turn])

    def parse_position(self, string):
        """
        Given a word describing a position on the board, give the X or Y value to which that word corresponds.
        :param string: single word, such as "top", "middle", or "right".
        """
        if string in ("top", "left"):
            return 0
        elif string in ("middle", "center"):
            return 1
        elif string in ("bottom", "right"):
            return 2
        else:
            return None

    def check_win(self):
        # TODO I am so tired
        if self.board[0][0] == self.board[0][1] == self.board[0][2] or \
                self.board[1][0] == self.board[1][0] == self.board[1][2] or \
                self.board[2][0] == self.board[2][1] == self.board[2][2] or \
                self.board[0][0] == self.board[1][0] == self.board[2][0] or \
                self.board[0][1] == self.board[1][1] == self.board[2][1] or \
                self.board[0][2] == self.board[1][2] == self.board[2][2] or \
                self.board[0][0] == self.board[1][1] == self.board[2][2] or \
                self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return True
        return False

    def response(self, query, name):
        #super().response(query)
        parameters = query.split(" ")
        command = parameters.pop(0)
        if command == "start":
            if self.started:
                return "A game is already in progress!"
            elif len(parameters) == 0:
                return "Please specify your opponent."
            else:
                return self.start_game(players=[name, " ".join(parameters)[1:]])
        elif command == "cancel":
            if self.started:
                return self.cancel_game()
            else:
                return "No game is in progress."
        elif command == "place":
            if name != self.players[self.turn]:
                return "You didn't really think I wouldn't have checked that you're the right person? Try harder, fool. It's %s's turn." % self.players[self.turn]
            x = self.parse_position(parameters.pop(0))
            y = self.parse_position(parameters.pop(0))
            return self.place(x, y)
        else:
            return "Invalid action."

if __name__ == "__main__":
    ttt = TicTacToe()
    print(ttt.response("start @Crista Falk", "Erik Bøsen"))
    while True:
        print(ttt.response(input("> "), 'Erik Bøsen'))

