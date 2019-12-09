from board import TicTacToe
import numpy as np
from copy import deepcopy
import pickle
import random
import time

model = pickle.load(open('dnn_model.pkl', 'rb'))

def bestMove(board, model, player, rnd=0):
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
            winPrediction = prediction[1]
            lossPrediction = prediction[2]
        else:
            winPrediction = prediction[2]
            lossPrediction = prediction[1]
        drawPrediction = prediction[0]

        if winPrediction - lossPrediction > 0:
            scores.append(winPrediction - lossPrediction)
        else:
            scores.append(drawPrediction - lossPrediction)

    # Choose the best move with a random factor
    bestMoves = np.flip(np.argsort(scores))
    for i in range(len(bestMoves)):
        if random.random() * rnd < 0.5:
            return moves[bestMoves[i]]

    # Choose a move completely at random
    return moves[random.randint(0, len(moves) - 1)]

def getPlayerMove():
    row = int(input("Enter the row that you want to play on (1, 2, or 3): ")) - 1
    col = int(input("Now enter the column that you want to play on (1, 2, or 3): ")) - 1
    print("\n")

    return row, col

def idiotCheck(i=0):
    row, col = getPlayerMove()
    if (i > 2):
        print("You've failed too many times. This game is ending")
        return "break","break"
    if row not in [0,1,2] or col not in [0,1,2]:
        print("What you entered is not 1, 2, or 3. Try again")
        board.print_board()
        i += 1
        return idiotCheck(i=i)
    if board.current_board[row, col] != ' ':
        print("That space on the board is already taken. Try again")
        board.print_board()
        i += 1
        return idiotCheck(i=i)
    return row, col


playAgain = 'y'
while playAgain == 'y':
    skip = False
    game_data = dict(moves=list(), board_history=list(), winner=None)

    var = int(input("Would you like to go first or second? Enter 1 for first, 2 for 2nd: "))
    print("\n")

    if var not in [1,2]:
        print("You didn't enter either 1 or 2...")
        skip = True

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

        if board.player - var == -1:

            row, col = idiotCheck()

            if row == "break":
                break

            move_ind = (row, col)

            board.move(*move_ind)

            board.print_board()
        else:
            time.sleep(1)
            print("My turn: ")
            time.sleep(1)
            move_ind = bestMove(board, model, board.player, 0)
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
            if board.player == var-1:
                print("You win!")
            else:
                print("You're an idiot lol")

        game_data['moves'].append((board.player, move_ind))
        game_data['board_history'].append(deepcopy(board.current_board))
        board.next_player()

    playAgain = input("Would you like to play again? (y/n)")
    print("\n")
