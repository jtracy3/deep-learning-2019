import numpy as np

class TicTacToe():

    def __init__(self):
        self.setup_board = np.zeros((3, 3), dtype='str')
        self.setup_board[self.setup_board == ''] = ' '
        self.current_board = self.setup_board
        self.player = 0
        self.player_map = {0: 'X', 1: 'O'}

    def print_board(self):
        for line in self.current_board:
            print(line)

    def move(self, row, column):
        if self.current_board[row, column] != ' ':
            raise Exception('Invalid placement')
        self.current_board[row, column] = self.player_map[self.player]

    def check_winner(self):
        n_rows, n_cols = self.current_board.shape
        if self.player_map[self.player] == 'X':
            for row in range(n_rows):
                for col in range(n_cols):
                    if self.current_board[row, col] != ' ':
                        try:
                            if self.current_board[row, col] == 'X'\
                                    and self.current_board[row + 1, col] == 'X'\
                                    and self.current_board[row + 2, col] == 'X':
                                return True
                        except IndexError:
                            pass

                        try:
                            if self.current_board[row, col] == 'X' \
                                    and self.current_board[row, col + 1] == 'X' \
                                    and self.current_board[row, col + 2] == 'X':
                                return True
                        except IndexError:
                            pass

                        try:
                            if self.current_board[row, col] == 'X' \
                                    and self.current_board[row + 1, col + 1] == 'X' \
                                    and self.current_board[row + 2, col + 2] == 'X':
                                return True
                        except IndexError:
                            pass

                        try:
                            if self.current_board[row, col] == 'X' \
                                    and self.current_board[row + 1, col - 1] == 'X' \
                                    and self.current_board[row + 2, col - 2] == 'X':
                                return True
                        except IndexError:
                            pass

        if self.player_map[self.player] == 'O':
            for row in range(n_rows):
                for col in range(n_cols):
                    if self.current_board[row, col] != ' ':
                        try:
                            if self.current_board[row, col] == 'O'\
                                    and self.current_board[row + 1, col] == 'O'\
                                    and self.current_board[row + 2, col] == 'O':
                                return True
                        except IndexError:
                            pass

                        try:
                            if self.current_board[row, col] == 'O' \
                                    and self.current_board[row, col + 1] == 'O' \
                                    and self.current_board[row, col + 2] == 'O':
                                return True
                        except IndexError:
                            pass

                        try:
                            if self.current_board[row, col] == 'O' \
                                    and self.current_board[row + 1, col + 1] == 'O' \
                                    and self.current_board[row + 2, col + 2] == 'O':
                                return True
                        except IndexError:
                            pass

                        try:
                            if self.current_board[row, col] == 'O' \
                                    and self.current_board[row + 1, col - 1] == 'O' \
                                    and self.current_board[row + 2, col - 2] == 'O':
                                return True
                        except IndexError:
                            pass

    def possible_actions(self):
        n_rows, n_cols = self.current_board.shape
        actions = []
        for row in range(n_rows):
            for col in range(n_cols):
                if self.current_board[row, col] == ' ':
                    actions.append((row, col))
        return actions

    def next_player(self):
        self.player = (self.player + 1) % 2

    def play_game(self, type='random'):
        moves = 0
        play = True
        random = np.random
        actions = self.possible_actions()
        # if type != 'random':
        # actions = [(0, 0), (0, 1), (0, 2),
        #            (1, 0), (1, 1), (1, 2),
        #            (2, 0), (2, 1), (2, 2)]
        while play:
            m = len(actions)
            pick = random.randint(0, m)
            move_ind = actions.pop(pick)
            self.move(*move_ind)
            self.print_board()
            if self.check_winner():
                play = False
                print(f'Player {self.player} is the winner!')
            elif not self.check_winner() and self.possible_actions() == []:
                play = False
                print(f'Draw')
            self.next_player()
            moves += 1

# tic_tac_toe = TicTacToe()
# tic_tac_toe.print_board()
# tic_tac_toe.play_game()

