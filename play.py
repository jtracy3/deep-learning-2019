from board import TicTacToe
import numpy as np
from copy import deepcopy
import pickle
import random

ttt_model = pickle.load(open('dnn_model.pkl', 'rb'))


def best_move(board, model, player, rnd=0):
    scores = []
    moves = board.possible_actions()

    # Make predictions for each possible move
    for i in range(len(moves)):
        future = deepcopy(board)
        future.move(*moves[i])

        flattened_board = np.array(future.flatten_board())
        flattened_board = flattened_board.reshape((-1,9))
        prediction = model.predict(flattened_board)[0]
        if player == 0:
            win_prediction = prediction[1]
            loss_prediction = prediction[2]
        else:
            win_prediction = prediction[2]
            loss_prediction = prediction[1]
        draw_prediction = prediction[0]

        if win_prediction - loss_prediction > 0:
            scores.append(win_prediction - loss_prediction)
        else:
            scores.append(draw_prediction - loss_prediction)

    # Choose the best move with a random factor
    best_moves = np.flip(np.argsort(scores))
    for i in range(len(best_moves)):
        if random.random() * rnd < 0.5:
            return moves[best_moves[i]]

    # Choose a move completely at random
    return moves[random.randint(0, len(moves) - 1)]


def play_game(p1=None, p2=None, rnd=0):
    game_data = dict(moves=list(), board_history=list(), winner=None)
    board = TicTacToe()
    play = True
    actions = board.possible_actions()
    while play and actions:
        actions = board.possible_actions()
        m = len(actions)
        if board.player == 0 and p1 is not None:
            move_ind = best_move(board, p1, board.player, rnd)
            board.move(*move_ind)
        elif board.player == 1 and p2 is not None:
            move_ind = best_move(board, p2, board.player, rnd)
            board.move(*move_ind)
        else:
            pick = np.random.randint(0, m)
            move_ind = actions[pick]
            board.move(*move_ind)
        a_winner, reward = board.check_winner()
        if a_winner and reward != 0:
            play = False
            game_data['winner'] = board.player
        elif a_winner and reward == 0:
            play = False
            game_data['winner'] = 0.5
        game_data['moves'].append((board.player, move_ind))
        game_data['board_history'].append(deepcopy(board.current_board))
        board.next_player()
    board.print_board()
    print(game_data['winner'])
    return game_data


def gather_game_results(n_games, p1=None, p2=None, rnd=0):
    results = dict(x_wins=0, o_wins=0, draws=0)
    for i in range(n_games):
        sim_game = play_game(p1=p1,p2=p2,rnd=rnd)
        if sim_game['winner'] == 0:
            results['x_wins'] += 1
        elif sim_game['winner'] == 1:
            results['o_wins'] += 1
        else:
            results['draws'] += 1
    x_win_pct = results['x_wins'] / n_games
    o_win_pct = results['o_wins'] / n_games
    draw_pct = results['draws'] / n_games

    print(f'The winning percentage for X was {x_win_pct*100:.1f}% in {n_games} random simulations')
    print(f'The winning percentage for O was {o_win_pct*100:.1f}% in {n_games} random simulations')
    print(f'The percentage of draws was {draw_pct*100:.1f}% in {n_games} random simulations')


game_data = play_game(p1=ttt_model)
print(game_data)

gather_game_results(100, p1=ttt_model)

# def gather_game_results(n_games):
#     results = dict(x_wins=0, o_wins=0, draws=0)
#     for i in range(n_games):
#         sim_game = play_game()
#         if sim_game['winner'] == 0:
#             results['x_wins'] += 1
#         elif sim_game['winner'] == 1:
#             results['o_wins'] += 1
#         else:
#             results['draws'] += 1
#     x_win_pct = results['x_wins'] / n_games
#     o_win_pct = results['o_wins'] / n_games
#     draw_pct = results['draws'] / n_games
#
#     print(f'The winning percentage for X was {x_win_pct*100:.2f}% in {n_games} random simulations')
#     print(f'The winning percentage for O was {o_win_pct*100:.2f}% in {n_games} random simulations')
#     print(f'The percentage of draws was {draw_pct*100:.2f}% in {n_games} random simulations')

# gather_game_results(10000)

# def simulate_games(n_iter):
#     results = dict(data=[], value=[], n_moves=[])
#     for i in range(n_iter):
#         sim_game = play_game()
#         results['data'].append(sim_game[0])
#         results['value'].append(sim_game[1])
#         results['n_moves'].append(sim_game[2q])
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
