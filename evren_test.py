import numpy as np
import copy as c
import random
from collections import defaultdict

from transformations import *
from board import *


def ai_if_symmetrical(board):
    board_refl_vert = np.dot(board, refl)
    board_refl_diag = np.dot(board, transformations[7])

    VERT_SYMMETRY = 0
    DIAG_SYMMETRY = 0

    if np.array_equal(board, board_refl_vert):
        VERT_SYMMETRY = 1
    if np.array_equal(board, board_refl_diag):
        DIAG_SYMMETRY = 1


    if VERT_SYMMETRY == 1:
        for i in range(3):
            if board[2 + 3 * i] == 1:
                board[2 + 3 * i] = 0

    if DIAG_SYMMETRY == 1:
        if board[3] == 1:
            board[3] = 0
        if board[6] == 1:
            board[6] = 0
        if board[7] == 1:
            board[7] = 0

def ai_decision(board, forbidden_pos, sign):
    sboard = board2str(board, sign)

    for p in forbidden_pos[sboard]:
        board[p] = 0

    choose_list = list()
    for i in range(len(board)):
        if board[i] == 1:
            choose_list.append(i)

    return random.choice(choose_list)


def main():
    board = np.array([64, 8, 1, 16, 1, 4, 1, 32, 2])
    
    for _  in range(1000):
        np.random.shuffle(board)

        wo = if_force_win(board, 0)
        wx = if_force_win(board, 1)

        if wo != -1:
            tmp_board = c.copy(board)
            place_sign(board, wo, 0)
            if if_game_end(board) == -1:
                print('Warning!')
                board_print(tmp_board)
                print(wo)
                board_print(board)
                input()

        if wx != -1:
            tmp_board = c.copy(board)
            place_sign(board, wx, 1)
            if if_game_end(board) == -1:
                print('Warning!')
                board_print(tmp_board)
                print(wx)
                board_print(board)
                input()

    return 0

    # sboard='0020326448160'
    # board = str2board(sboard)[0]
    #
    # board_print(board)
    # board_print_sign(board)
    # return 0

    board = np.array([64, 8, 1, 16, 1, 4, 1, 32, 2])
    print(board2str(transform_board(board)[0], 1))
    board_print(transform_board(board)[0])

    return 0

    forbidden_pos = defaultdict(set)
    sign = 0


    while True:
        # np.random.shuffle(board)

        board_print(board)

        tran = find_transformation(board)
        tran_board = np.dot(board, transformations[tran])

        board_print(tran_board)

        print(tran)
        ai_move = ai_decision(tran_board, forbidden_pos, sign)
        print(ai_move)
        ai_move_orig = np.argmax(transformations[tran][:, ai_move:ai_move + 1])  # ai_move-nak megfelelő sorban levő 1-es helye

        print(ai_move_orig)

        place_sign(board, ai_move_orig, sign)

        board_print(board)
        input()
        print('\n\n\n')



    # board = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    board = np.array([16, 32, 64, 0, 0, 0, 0, 0, 0])

    f = set() # 48
    s = set() # 504
    print(board)
    for _ in range(10000):
        np.random.shuffle(board)
        sb = board2str(board, 0)
        s.add(sb)
        game = if_game_end(board)
        if game == 0 or game == 1:
            if s not in f:
                f.add(sb)

    print(len(s))
    print(len(f))

    return 0
    for _ in range(10):
        np.random.shuffle(board)
        game = if_game_end(board)
        if game == 0 or game == 1:
            board_print_sign(list(board))
            print('\n')

    return 0

    # TRANSZFORMÁCIÓK MŰKÖDÉSÉNEK ELLENŐRZÉSE
    board = np.array([2, 4, 0, 0, 0, 0, 0, 0, 0])

    np.random.shuffle(board)
    print("Kiindulási tábla")
    board_print(board)
    print()

    t = find_transformation(board)

    board = np.dot(board, transformations[t])
    print("Kezdetben helyretranszformált változata")
    board_print(board)

    for i in range(20000):
        for j in range(8):
            tmp_board = c.copy(board)
            tmp_board = np.dot(board, transformations[j])
            t_tmp = find_transformation(tmp_board)
            tmp_board = np.dot(tmp_board, transformations[t_tmp])

            # print(tmp_board, end='\n')
            if not np.array_equal(tmp_board, board):
                board_print(board)

    print("OK")

    return 0

    d = defaultdict(list)
    pos = 'asd'
    pos2 = 'qwe'

    d[pos].append(0)
    print(d)

    d[pos].append(1)
    print(d)

    d[pos2].append(3)
    print(d)

    for s in d:
        print(s, d[s])

    sign = 0
    board = np.array([32, 64, 0, 16, 2, 4, 0, 8, 0], dtype='int32')
    print(board)
    print(sign)

    sboard = board2str(board, sign)
    print(sboard)
    board2, sign2 = str2board(sboard)
    print(str2board(sboard))
    print(board2)
    print(sign2)
    print(np.array_equal(board, board2))

    return 0

    sign = 0
    s = 0
    ch = ""
    # board = np.arange(1, 7, 1)
    # board = np.concatenate( ( board, np.array([0, 0, 0]) ) )
    test = np.zeros(9, dtype='int32')
    board = np.array([32, 64, 0, 16, 2, 4, 0, 8, 0], dtype='int32')

    print(board)
    sboard = board2str(board)
    print(sboard)
    print(str2board(sboard))
    return 0
    while ch != 'q' and ch != 'Q':
        board_print(board)
        print(sign)
        print(s)
        print(board)
        print(np.append(board, sign))
        ch = input()
        if ch == 'r' or ch == 'R':
            s = 0
            clrscr()
            continue
        pos = int(ch)
        s += 1
        place_sign(board, pos, sign)
        sign = (sign + 1) % 2
        clrscr()


main()
