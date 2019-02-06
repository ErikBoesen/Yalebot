#from .base import Module
import re


class Game():#Module):
    def __init__(self):
        self.started = False

    def response(self, query, name):
        """
        Handle general game starting, cancelling, etc. logic.
        """
        pass


class TicTacToe(Game):
    EMPTY = '-'
    PLAYER_X = 'X'
    PLAYER_O = 'O'
    size = 3
    started = False

    def init_board(self):
        self.board = {}
        for x in range(self.size):
            for y in range(self.size):
                self.board[(x, y)] = EMPTY
        return self.board

    def print_board(self):
        for coord in sorted(self.board.keys()):
            x, y = coord
            if y == 0 and x != 0:           # if is new row
                print('\n' + '-' * 2* len(self.board))

            val = self.board[coord]
            if val is not EMPTY:
                print(" %s |" % (val), end="")
            else:
                print("%1d,%1d|" % (coord), end="")

    def place_piece(self, coord, player):
        if coord in self.board.keys() and self.board[coord] is EMPTY:
            self.board[coord] = player
            return True
        else:
            return False

    def has_won(self, player):
        for n in range(self.size):
            rows = [board[(x, y)] for x, y in sorted(board.keys()) if n is x]
            cols = [board[(x, y)] for x, y in sorted(board.keys()) if n is y]
            diagonals = [board[(x, y)] for x, y in sorted(board.keys()) if x is y]
            if rows.count(player) is size or cols.count(player) is size or diagonals.count(player) is size:
                return True
        return False

    def board_full(self):
        return list(self.board.values()).count(EMPTY) == 0

    def game_ended(self):
        return board_full() or has_won(PLAYER_X) or has_won(PLAYER_O)

    def game_winner(self):
        if self.has_won(self.size, PLAYER_X):
            return PLAYER_X
        elif self.has_won(self.size, PLAYER_O):
            return PLAYER_O
        elif self.board_full():
            return None

    def valid_move(self, user_in):
        user_in = user_in.strip()
        matches = re.match(r"[0-9]+\s*,\s*[0-9]+", user_in)
        if matches is not None:
            return tuple(map(int, user_in.split(',')))
        else:
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
                self.board = self.init_board(self.size)
                print("\n*****************************************")
                print("Let's play some tic tac toe!")
                print("X: Player X, O: Player O, (x,y): Empty spot")
                print("Enter coordinate in empty spot to fill it\n")

                self.print_board(self.board)
                self.turn = PLAYER_O
        elif command == "cancel":
            if self.started:
                return self.cancel_game()
            else:
                return "No game is in progress."
        elif command == "place":
            #if name != self.players[self.turn]:
            #    return "You didn't really think I wouldn't have checked that you're the right person? Try harder, fool. It's %s's turn." % self.players[self.turn]
            user_in = input("Player " +  turn + ", place your piece: ")
            coord = valid_move(user_in)

            if coord and place_piece(coord, turn):
                print_board(board)
                #switch turns
                turn = PLAYER_X  if turn is PLAYER_O else PLAYER_O
            else:
                print("Invalid move.")
            if self.game_ended(size):
                print("Winner: " + self.game_winner(size))
        else:
            return "Invalid action."

if __name__ == "__main__":
    ttt = TicTacToe()
    print(ttt.response("start @Crista Falk", "Erik Bøsen"))
    while True:
        print(ttt.response(input("> "), 'Erik Bøsen'))

