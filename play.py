from board import TicTacToe
import board_encoder as enc
import numpy as np
from copy import deepcopy

def play_game():
    moves = 0
    board = TicTacToe()
    dataset = []
    play = True
    value = None
    while play and board.possible_actions() != []:
        actions = board.possible_actions()
        m = len(actions)
        pick = np.random.randint(0, m)
        move_ind = actions[pick]
        board.move(*move_ind)
        board.print_board()
        print('------------')
        if board.check_winner():
            play = False
            if board.player == 0:
                value = 1
            elif board.player == 1:
                value = -1
            print(f'Player {board.player} is the winner!')
        elif not board.check_winner() and board.possible_actions() == []:
            play = False
            value = 0
            print(f'Draw')
        print(board.current_board)
        dataset.append((deepcopy(board.current_board), board.player))
        board.next_player()
        moves += 1
    return dataset, value, moves

def simulate_games(n_iter):
    results = dict(data=[], outcome=[], n_moves=[])
    for i in range(n_iter):
        sim_game = play_game()
        results['data'].append(sim_game[0])
        results['outcome'].append(sim_game[1])
        results['n_moves'].append(sim_game[2])
    return results

results = simulate_games(10)
print(results)