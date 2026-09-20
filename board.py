import numpy as np
import copy as c
import os



def clrscr():
    os.system('cls' if os.name == 'nt' else 'clear')


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
    o = np.array([2, 4, 8])
    x = np.array([16, 32, 64])

    tmp_board = c.copy(board)
    tmp_matrix = np.reshape(tmp_board, (3, 3))

    # Sorok és oszlopok ellenőrzése
    for i in range(3):
        row = tmp_matrix[i:i + 1]
        col = tmp_matrix[:, i:i + 1]

        if np.isin(row, o).all() or np.isin(col, o).all():
            return 0
        elif np.isin(row, x).all() or np.isin(col, x).all():
            return 1

    # Átlók ellenőrzése
    diag_main = np.diag(tmp_matrix)
    diag_sec = np.fliplr(tmp_matrix).diagonal()

    if np.isin(diag_main, o).all() or np.isin(diag_sec, o).all():
        return 0
    elif np.isin(diag_main, x).all() or np.isin(diag_sec, x).all():
        return 1

    return -1


# Van-e nyerő lépés
def if_force_win(board, signal):
    if signal == 0:
        own = np.array([2, 4, 8])
        enemy = np.array([16, 32, 64])
    elif signal == 1:
        enemy = np.array([2, 4, 8])
        own = np.array([16, 32, 64])


    tmp_board = np.ones(9, dtype='int32')
    for i in range(9):
        if signal == 0:
            if board[i] != 8:
                tmp_board[i] = board[i]
        elif signal == 1:
            if board[i] != 64:
                tmp_board[i] = board[i]

    tmp_matrix = np.reshape(tmp_board, (3, 3))

    # Sorok és oszlopok ellenőrzése
    for i in range(3):
        row = tmp_matrix[i:i + 1]
        col = tmp_matrix[:, i:i + 1]

        # board_print(board)
        # print(row)
        # print('row[0]:', row[0])
        # print(row[0][2])

        # print(col)
        # print(col[0])

        row_signal = 0
        col_signal = 0
        win_pos_row = -1
        win_pos_col = -1

        for k in range(3):
            if np.isin(row[0][k], own).all():
                row_signal += 1
            elif not np.isin(row[0][k], enemy).all():
                win_pos_row = k
            if np.isin(col[k][0], own).all():
                col_signal += 1
            elif not np.isin(col[k][0], enemy).all():
                win_pos_col = k

        if row_signal == 2 and win_pos_row != -1:
            print('ROW', i, win_pos_row)
            return win_pos_row + 3 * i
        if col_signal == 2 and win_pos_col != -1:
            print('COL', i, win_pos_col, col_signal)
            return 3 * win_pos_col + i


    # Átlók ellenőrzése
    diag_main_signal = 0
    diag_sec_signal = 0
    win_pos_diag_main = -1
    win_pos_diag_sec = -1

    for k in range(3):
        # Főátló
        if np.isin(tmp_matrix[k, k], own).all():
            diag_main_signal += 1
        elif not np.isin(tmp_matrix[k, k], enemy).all():
            win_pos_diag_main = k

        # Mellékátló
        if np.isin(tmp_matrix[k, 2 - k], own).all():
            diag_main_signal += 1
        elif not np.isin(tmp_matrix[k, 2 - k], enemy).all():
            win_pos_diag_main = k


    if diag_main_signal == 2 and win_pos_diag_main != -1:
        print('DIAG MAIN', win_pos_diag_main)
        return 4 * win_pos_diag_main
    if diag_sec_signal == 2 and win_pos_diag_sec != -1:
        print('DIAG SEC', win_pos_diag_sec)
        return 2 * win_pos_diag_sec + 2

    return -1
