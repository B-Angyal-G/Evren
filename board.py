import numpy as np

def board_print(board_vector):
    print(np.reshape(board_vector, (3, 3)))

def board2str(board, sign):
    s = ""
    for i in board:
        s += str(i)
    return s + str(sign)

def str2board(str_board):
    board = np.zeros(9, dtype='int32')
    s = 0
    for i in range(len(board)):
        if str_board[s] in {'2', '4', '8'}:
            board[i] = int(str_board[s])
        elif str_board[s] == '1':
            board[i] = 16
            s += 1
        elif str_board[s] == '3':
            board[i] = 32
            s += 1
        elif str_board[s] == '6':
            board[i] = 64
            s += 1
        s += 1
    
    return (board, int(str_board[-1]))

def place_sign(board, position, sign):
    # SIGN 0: O
    #      1: X

    # Kör: 2, 4, 8
    if sign == 0:
        for i in range(9):
            if i == position:
                board[i] = 2

            elif board[i] in (2, 4):
                board[i] *= 2

            elif board[i] == 8:
                board[i] = 0

    # X: 16, 32, 64
    if sign == 1:
        for i in range(9):
            if i == position:
                board[i] = 16

            elif board[i] in (16, 32):
                board[i] *= 2

            elif board[i] == 64:
                board[i] = 0
                
def add_forbiddenpos(forbiddens, sboard, pos):
    pass

