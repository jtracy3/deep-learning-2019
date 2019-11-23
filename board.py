import numpy as np

class TicTacToe():

    def __init__(self):
        self.board = np.zeros((3, 3), dtype='str')
        self.current_board = self.board
        self.player = {0: 'X', 1: 'O'}

    def print_board(self):
        for line in self.board:
            print(line)

    def move(self, row, column, playerId):
        if self.board[row, column] != '':
            raise Exception('Invalid placement')
        self.board[row, column] = self.player[playerId]

    def check_winner(self, playerId):
        n_rows, n_cols = self.board.shape
        if self.player[playerId] == 'X':
            for row in range(n_rows):
                for col in range(n_cols):
                    if self.board[row, col] != '':
                        try:
                            if self.board[row, col] == 'X'\
                                    and self.board[row + 1, col] == 'X'\
                                    and self.board[row + 2, col] == 'X':
                                return True
                        except IndexError:
                            pass

                        try:
                            if self.board[row, col] == 'X' \
                                    and self.board[row, col + 1] == 'X' \
                                    and self.board[row, col + 1] == 'X':
                                return True
                        except IndexError:
                            pass

                        try:
                            if self.board[row, col] == 'X' and self.board



tic_tac_toe = TicTacToe()
tic_tac_toe.print_board()
tic_tac_toe.move(1, 1, 0)
tic_tac_toe.print_board()
tic_tac_toe.move(2, 1, 1)
