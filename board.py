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

    def check_winner_reward(self):
        """Checks if the game is over and return a possible winner.
        There are 3 possible scenarios
            a) The game is over and we have a winner.
            b) The game is over but it is a draw.
            c) The game is not over.
        Args:
            current_player: An integer representing the current player.
        Returns:
            A bool representing the game over state.
            An integer action value. (win: 1, loss: -1, draw: 0
        """
        n_rows, n_cols = self.current_board.shape

        player_a = self.player
        player_b = (self.player + 1) % 2

        # Check for horizontal marks
        for x in range(n_rows):
            player_a_count = 0
            player_b_count = 0
            for y in range(n_cols):
                if self.current_board[x][y] == self.player_map[player_a]:
                    player_a_count += 1
                elif self.current_board[x][y] == self.player_map[player_b]:
                    player_b_count += 1
            if player_a_count == n_cols:
                return True, 1
            elif player_b_count == n_cols:
                return True, -1

        # Check for vertical marks
        for x in range(n_rows):
            player_a_count = 0
            player_b_count = 0
            for y in range(n_cols):
                if self.current_board[y][x] == self.player_map[player_a]:
                    player_a_count += 1
                elif self.current_board[y][x] == self.player_map[player_b]:
                    player_b_count += 1
            if player_a_count == n_rows:
                return True, 1
            elif player_b_count == n_rows:
                return True, -1

        # Check for major diagonal marks
        player_a_count = 0
        player_b_count = 0
        for x in range(n_rows):
            if self.current_board[x][x] == self.player_map[player_a]:
                player_a_count += 1
            elif self.current_board[x][x] == self.player_map[player_b]:
                player_b_count += 1

        if player_a_count == n_rows:
            return True, 1
        elif player_b_count == n_rows:
            return True, -1

        # Check for minor diagonal marks
        player_a_count = 0
        player_b_count = 0
        for y in range(n_rows - 1, -1, -1):
            x = 2 - y
            if self.current_board[x][y] == self.player_map[player_a]:
                player_a_count += 1
            elif self.current_board[x][y] == self.player_map[player_b]:
                player_b_count += 1

        if player_a_count == n_rows:
            return True, 1
        elif player_b_count == n_rows:
            return True, -1

        # There are still moves left so the game is not over
        actions = self.possible_actions()
        if not actions:
            return False, 0

        # If there are no moves left the game is over without a winner
        return True, 0

    def next_player(self):
        self.player = (self.player + 1) % 2
