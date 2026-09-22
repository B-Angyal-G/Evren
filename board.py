import numpy as np
import copy as c
import os



def clrscr():
    os.system('cls' if os.name == 'nt' else 'clear')


# Tábla kiíratása számokkal és jelekkel
def board_print(board):
    print(np.reshape(board, (3, 3)))
    print()


def board_print_sign(board):
    tmp_board = np.array(['.', '.', '.', '.', '.', '.', '.', '.', '.'])
    o = {2, 4, 8}
    x = {16, 32, 64}

    for i in range(len(board)):
        if board[i] in o:
            tmp_board[i] = 'o'
        elif board[i] in x:
            tmp_board[i] = 'x'
        elif board[i] == 0:
            tmp_board[i] = '.'

    print(np.reshape(tmp_board, (3, 3)))
    print()


# Állás mentéséhez szükséges string előállítása
def board2str(board, sign):
    s = ""
    for i in board:
        if i > 1:
            s += str(i)
        else:
            s += '0'
    return s + str(sign)


# Mentett string-ből tábla visszaállítása
def str2board(str_board):
    board = np.ones(9, dtype='int32')
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


# Megfelelő jel elhelyezése
def place_sign(board, position, sign):
    # SIGN 0: O
    #      1: X

    # Kör: 2, 4, 8
    if sign == 0:
        for i in range(9):
            if i == position:
                board[i] = 2
            elif board[i] == 2 or board[i] == 4:
                board[i] *= 2
            elif board[i] == 8 or board[i] == 0:
                board[i] = 1

    # X: 16, 32, 64
    if sign == 1:
        for i in range(9):
            if i == position:
                board[i] = 16
            elif board[i] == 16 or board[i] == 32:
                board[i] *= 2
            elif board[i] == 64 or board[i] == 0:
                board[i] = 1


# Nyert-e valaki? Visszatérés: 0 -> o, 1 -> x, egyébként -1
def if_game_end(board):
    tmp_board = c.copy(board)
    tmp_matrix = np.reshape(tmp_board, (3, 3))

    # Sorok és oszlopok ellenőrzése
    for i in range(3):
        row = tmp_matrix[i:i + 1]
        col = tmp_matrix[:, i:i + 1]

        if np.sum(row) == 14 or np.sum(col) == 14:
            return 0
        elif np.sum(row) == 112 or np.sum(col) == 112:
            return 1

    # Átlók ellenőrzése
    diag_main = np.diag(tmp_matrix)
    diag_sec = np.fliplr(tmp_matrix).diagonal()

    if np.sum(diag_main) == 14 or np.sum(diag_sec) == 14:
        return 0
    elif np.sum(diag_main) == 112 or np.sum(diag_sec) == 112:
        return 1

    return -1


# Van-e nyerő lépés egy adott jelnek: igen -> pos, egyébként -1
def if_force_win(board, signal):
    tmp_board = np.zeros(9, dtype='int32')
    if signal == 0:
        limit_min = 6
        limit_max = 12
        for i in range(9):
            if board[i] != 8 and board[i] > 1:
                tmp_board[i] = board[i]

    elif signal == 1:
        limit_min = 48
        limit_max = 96
        for i in range(9):
            if board[i] != 64 and board[i] > 1:
                tmp_board[i] = board[i]

    tmp_matrix = np.reshape(tmp_board, (3, 3))

    # Sorok és oszlopok ellenőrzése
    for i in range(3):
        row = tmp_matrix[i:i + 1]
        col = tmp_matrix[:, i:i + 1]

        sum_row = np.sum(row)
        sum_col = np.sum(col)

        if sum_row >= limit_min and sum_row <= limit_max:
            for k in range(3):
                if row[0][k] == 0 or row[0][k] == 1:
                    # print(tmp_matrix)
                    # print('Win row:', signal, i, k)
                    # print()
                    return 3 * i + k

        if sum_col >= limit_min and sum_col <= limit_max:
            for k in range(3):
                if col[k][0] == 0 or col[k][0] == 1:
                    # print(tmp_matrix)
                    # print('Win col:', signal, i, k)
                    # print()
                    return 3 * k + i

    # Átlók ellenőrzése
    diag_main = np.diag(tmp_matrix)
    diag_sec = np.fliplr(tmp_matrix).diagonal()

    sum_diag_main = np.sum(diag_main)
    sum_diag_sec = np.sum(diag_sec)

    if sum_diag_main >= limit_min and sum_diag_main <= limit_max:
        for k in range(3):
            if diag_main[k] == 0 or diag_main[k] == 1:
                # print(tmp_matrix)
                # print('Win diag main:', signal, k)
                # print()
                return 4 * k

    if sum_diag_sec >= limit_min and sum_diag_sec <= limit_max:
        for k in range(3):
            if diag_sec[k] == 0 or diag_sec[k] == 1:
                # print(tmp_matrix)
                # print('Win diag sec:', signal, k)
                # print()
                return 2 * k + 2

    return -1
