import numpy as np
from board import TicTacToe

def encode_board(TicTacToe, playerId):
    board_st = TicTacToe.current_board
    board_enc = np.zeros([3,3,3]).astype(int)
    for i in range(3):
        for j in range(3):
            if board_st[i, j] != ' ':
                if board_st[i, j] == 'X':
                    board_enc[i, j, 0] = 1
                elif board_st[i, j] == 'O':
                    board_enc[i, j, 1] = 1
    board_enc[:, :, 2] = playerId
    return board_enc

def decode_board(encoded_board):
    board_dec = np.zeros([3,3], dtype = 'str')
    board_dec[board_dec == ''] = ' '
    decode_dict = {0: 'X', 1: 'O'}
    for l in range(2):
        for i in range(3):
            for j in range(3):
                if encoded_board[i, j, l] == 1:
                    board_dec[i, j] = decode_dict[l]
    return board_dec


# Test a board and see what happens

tic_tac_toe = TicTacToe()
tic_tac_toe.move(1, 1, 0)
tic_tac_toe.move(2, 1, 1)
tic_tac_toe.move(0, 0, 0)
tic_tac_toe.move(2, 0, 1)
tic_tac_toe.print_board()

encoded = encode_board(tic_tac_toe, 0)

print(encoded[:, :, 0])
print(encoded[:, :, 1])
print(encoded[:, :, 2])

decoded = decode_board(encoded)

print(decoded)



