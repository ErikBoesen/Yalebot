from .base import Module


class TicTacToe(Module):
    DESCRIPTION = "Play a friendly game of tic tac toe"
    ARGC = 1
    players = [''] * 2
    board = [' '] * 9
    movements = {'a1': 0, 'a2': 1, 'a3': 2,
                 'b1': 3, 'b2': 4, 'b3': 5,
                 'c1': 6, 'c2': 7, 'c3': 8}
    turn = True    
    
    def clear(self):
        self.players = [''] * 2
        self.board = [' '] * 9
        self.turn = True
    
    def board(self):
        pboard = '|'.join(self.board[:3]) + '\n——————\n'
        pboard += '|'.join(self.board[3:6]) + '\n——————\n'
        pboard += '|'.join(self.board[6:])
        return pboard
    
    def check(self):
        #TODO: find a better way to check for three in a row
        check = [self.board[0:3], self.board[3:6], self.board[6:],
                 [self.board[0], self.board[3], self.board[6]],
                 [self.board[1], self.board[4], self.board[7]],
                 [self.board[2], self.board[5], self.board[8]],
                 [self.board[0], self.board[4], self.board[8]],
                 [self.board[2], self.board[4], self.board[6]]]
        for arr in check:
            if arr[:3] == ['x'] * 3:
                self.clear()
                return f'{self.players[0]} wins!'
            elif arr[:3] == ['o'] * 3:
                self.clear()
                return f'{self.players[1]} wins!'
        return ''
    
    def response(self, query, message):
        arguments = query.split()
        command = arguments.pop(0).lower()
        name = message["name"]
        if command == 'join':
            if self.players[0] == '':
                self.players[0] = name
                return f"{name} has joined, waiting on a second player"
            elif self.players[1] == '':
                self.players[1] = name
                return [f"{name} has joined, ready to play", self.board()]
            else:
                return f"Game full. {self.players[0]} & {self.players[1]} are playing!"
        elif command == 'end':
            self.clear()
        elif command == 'help':
            desc = 'Possible commands: help, join, end. Positions:\n'
            desc += '|'.join(['a1','a2','a3']) + '\n——————\n'
            desc += '|'.join(['b1','b2','b3']) + '\n——————\n'
            desc += '|'.join(['c1','c2','c3'])
            return desc
        elif command in self.movements:
            loc = self.movements[command]
            if self.turn and name == self.players[0]:
                self.turn = False
                self.board[loc] = 'x'
            elif not self.turn and name == self.players[1]:
                self.turn = True
                self.board[loc] = 'o'
            if self.check() != '':
                return self.check()
            return self.board()
        else:
            return "Unkown command."
