import numpy as np
import copy as c
from collections import defaultdict


forbidden_pos = defaultdict(list)



def board_print(board):
    print(np.reshape(board, (3, 3)))

def board_print_sign(board):
    o = {2, 4, 8}
    x = {16, 32, 64}

    for i in range(len(board)):
        if board[i] in o:
            board[i] = 'o'
        elif board[i] in x:
            board[i] = 'x'
        elif board[i] == 0:
            board[i] = '.'

    print(np.reshape(board, (3, 3)))

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
                
def add_forbiddenpos(forbidden_pos, sboard, pos):
    forbidden_pos[sboard].append(pos)

def if_game_end(board):
    o = np.array([2, 4, 8])
    x = np.array([16, 32, 64])

    tmp_board = c.copy(board)
    tmp_matrix = np.reshape(tmp_board, (3, 3))

    # Sorok és oszlopok ellenőrzése
    for i in range(3):
        row = tmp_matrix[i:i+1]
        col = tmp_matrix[:, i:i+1]

        # print(row)
        # print()
        # print(col)
        # print()

        if np.isin(row, o).all() or np.isin(col, o).all():
            return 0
        elif np.isin(row, x).all() or np.isin(col, x).all():
            return 1

    # Átlók ellenőrzése
    diag_main = np.diag(tmp_matrix)
    diag_sec = np.fliplr(tmp_matrix).diagonal()

    # print(diag_main)
    # print(diag_sec)
    # print()

    if np.isin(diag_main, o).all() or np.isin(diag_sec, o).all():
        return 0
    elif np.isin(diag_main, x).all() or np.isin(diag_sec, x).all():
        return 1

