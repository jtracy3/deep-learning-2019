from board import TicTacToe
import numpy as np
from copy import deepcopy
import pickle
import random
import time

dnn_model = pickle.load(open('dnn_dense_model2.pkl', 'rb'))

conv_model = pickle.load(open('dnn_conv_model2.pkl','rb'))

def best_move(board, model, player, rnd=0, flatten=True):
    scores = []
    moves = board.possible_actions()

    # Make predictions for each possible move
    for i in range(len(moves)):
        future = deepcopy(board)
        future.move(*moves[i])

        if flatten:
          current_board = np.array(future.flatten_board())
          current_board = current_board.reshape((-1,9))
        else:
          current_board = future.current_board
          # print(current_board)
          n_rows, n_cols = current_board.shape
          for i in range(n_rows):
            for j in range(n_cols):
              if current_board[i][j] == ' ':
                current_board[i][j] = 0
              elif current_board[i][j] == 'X':
                current_board[i][j] = 1
              elif current_board[i][j] == 'O':
                current_board[i][j] = 2
          current_board = current_board.reshape((-1, 3, 3, 1))

        prediction = model.predict(current_board)[0]
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

def get_player_move():
    row = int(input("Enter the row that you want to play on (1, 2, or 3): ")) - 1
    col = int(input("Now enter the column that you want to play on (1, 2, or 3): ")) - 1
    print("\n")

    return row, col


def idiot_check(i=0):
    row, col = get_player_move()
    if i > 2:
        print("You've failed too many times. This game is ending")
        return "break", "break"
    if row not in [0, 1, 2] or col not in [0, 1, 2]:
        print("What you entered is not 1, 2, or 3. Try again")
        board.print_board()
        i += 1
        return idiot_check(i=i)
    if board.current_board[row, col] != ' ':
        print("That space on the board is already taken. Try again")
        board.print_board()
        i += 1
        return idiot_check(i=i)
    return row, col

def number_check(num,max,j=0):
    if (num.isdigit()):
        if int(num) in range(1,max+1):
            return int(num)
    j+=1
    print("Invalid entry. Try again: ")
    return None



playAgain = 'y'
while playAgain == 'y':
    skip = False
    game_data = dict(moves=list(), board_history=list(), winner=None)
    valid = False
    while valid != True:
        valid = True
        opponent = input("\n Welcome to Pokemon Gym Tic Tac Toe. First, choose your opponent (enter the number next to opponent): \n (1) Charmander \n (2) Charmeleon \n (3) Charizard \n")
        opponent = number_check(opponent, 3)
        if opponent == None:
            valid = False
            continue

        if opponent == 1:
            flatten = None
            model_selected = None
        elif opponent == 2:
            flatten = True
            model_selected = dnn_model
        elif opponent == 3:
            flatten = False
            model_selected = conv_model

    valid = False
    while valid != True:
        valid = True
        var = input("Would you like to go first or second? Enter 1 for first, 2 for 2nd: ")
        print("\n")

        var = number_check(var, 2)
        if var == None:
            valid = False
            continue


    board = TicTacToe()
    if var == 1:
        print("Okay, you will be X's. You're up first: ")
        board.print_board()
    elif var == 2:
        print("Okay, you will be O's. I'll go first: ")

    play = True
    actions = board.possible_actions()
    while play and actions and not skip:
        actions = board.possible_actions()
        m = len(actions)

        if board.player - var == -1:

            row, col = idiot_check()

            if row == "break":
                break

            move_ind = (row, col)

            board.move(*move_ind)

            board.print_board()
        else:
            time.sleep(1)
            print("My turn: ")
            time.sleep(1)
            if model_selected == None:
                pick = np.random.randint(0, m)
                move_ind = actions[pick]
                board.move(*move_ind)
            else:

                move_ind = best_move(board, model_selected, board.player, 0, flatten)
                board.move(*move_ind)

            board.print_board()

        a_winner, reward = board.check_winner()
        if a_winner and reward != 0:
            play = False
            game_data['winner'] = board.player
            if board.player == var-1:
                print("You win!")
            else:
                print("You're an idiot lol")
        elif a_winner and reward == 0:
            play = False
            game_data['winner'] = 0.5

            print("Tie game.")

        game_data['moves'].append((board.player, move_ind))
        game_data['board_history'].append(deepcopy(board.current_board))
        board.next_player()

    playAgain = input("Would you like to play again? (y/n)")
    print("\n")
