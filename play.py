from board import TicTacToe
import numpy as np
from copy import deepcopy

def play_game():
    game_data = dict(moves=list(), board_history=list(), winner=None)
    board = TicTacToe()
    play = True
    while play and board.possible_actions() != []:
        actions = board.possible_actions()
        print(actions)
        m = len(actions)
        pick = np.random.randint(0, m)
        move_ind = actions[pick]
        board.move(*move_ind)
        if board.check_winner():
            play = False
            game_data['winner'] = board.player
        elif not board.check_winner() and board.possible_actions() == []:
            play = False
            game_data['winner'] = 0.5
        game_data['moves'].append((board.player, move_ind))
        game_data['board_history'].append(deepcopy(board.current_board))
        board.next_player()
    return game_data

# game_data = play_game()
# print(game_data)

def gather_game_results(n_games):
    results = dict(x_wins=0, o_wins=0, draws=0)
    for i in range(n_games):
        sim_game = play_game()
        if sim_game['winner'] == 0:
            results['x_wins'] += 1
        elif sim_game['winner'] == 1:
            results['o_wins'] += 1
        else:
            results['draws'] += 1
    x_win_pct = results['x_wins'] / n_games
    o_win_pct = results['o_wins'] / n_games
    draw_pct = results['draws'] / n_games

    print(f'The winning percentage for X was {x_win_pct*100:.2f}% in {n_games} random simulations')
    print(f'The winning percentage for O was {o_win_pct*100:.2f}% in {n_games} random simulations')
    print(f'The percentage of draws was {draw_pct*100:.2f}% in {n_games} random simulations')

# gather_game_results(1000)

# def simulate_games(n_iter):
#     results = dict(data=[], value=[], n_moves=[])
#     for i in range(n_iter):
#         sim_game = play_game()
#         results['data'].append(sim_game[0])
#         results['value'].append(sim_game[1])
#         results['n_moves'].append(sim_game[2])
#     return results

# def create_mock_data(results, n_states, seed=0):
#     tensors = list()
#     values = list()
#     np.random.seed(seed)
#     for i in n_states:
#         random_game_number = np.random.randint(n_states)
#         random_game = results['data'][random_game_number]
#         n_states_from_random_game = results['n_moves'][random_game_number]
#         game_value = results['value'][random_game_number]
#         random_state_number = np.random.randint(n_states_from_random_game)
#         random_state = random_game[random_state_number][0]
#         random_state_player = random_game[random_state_number][1]
#         encoded_board = encode.encode_board(random_state, random_state_player)
#         tensors.append(encoded_board)
#         values.append(game_value)
#
#     return tensors, values
