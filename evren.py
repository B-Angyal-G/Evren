import numpy as np
import copy as c
import time as t
import random

from collections import defaultdict

from transformations import *
from board import *


# Szimmetrikus-e az állás (legfeljebb első 3 lépésben)
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


def ai_decision(board, forbidden_pos, sign, n, LEARN, learning_forbidden_pos):
    if n < 4:
        ai_if_symmetrical(board)

    sboard = board2str(board, sign)

    for p in forbidden_pos.get(sboard, set()):
        board[p] = 0

    if LEARN == 1:
        for p in learning_forbidden_pos.get(sboard, set()):
            board[p] = 0

    choose_list = list()
    for i in range(len(board)):
        if board[i] == 1:
            choose_list.append(i)

    if choose_list != list():
        return random.choice(choose_list)
    else:
        return -1



def main():
    forbidden_pos = defaultdict(set)
    learning_forbidden_pos = defaultdict(set)
    LEARN = 1

    
    start_time = t.time()
    n_sum = 0
    br = 0
    for i in range(20000):
        board = np.ones(9, dtype='int32')
        board_last = np.ones(9, dtype='int32')
        board_last_before = np.ones(9, dtype='int32')

        steps = list()

        sign = 0
        BREAK = 0

        if i % 500 == 0:
            print(i)
            print('500-as számításideje:', t.time() - start_time)
            print('Összes lépés száma:', n_sum)
            print('Breakek száma:', br)
            print()
            n_sum = 0
            br = 0
            start_time = t.time()

        n = 0
        while if_game_end(board) == -1:
            if n == 1000:
                # print('steps:', n + 1)
                br += 1
                BREAK = 1
                break

            transformed_board, tran = transform_board(board)

            ai_move = ai_decision(transformed_board, forbidden_pos, sign, n, LEARN, learning_forbidden_pos)
            if ai_move == -1:
                # print("BREAK")
                # board_print(board)
                # print(sign)
                # board_print(board_last)
                # board_print(board_last_before)
                # print(steps)
                # print('\n')
                break

            ai_move_orig = np.argmax(transformations[tran][:, ai_move:ai_move + 1])    # ai_move-nak megfelelő oszlopban levő 1-es helye

            board_last_before = c.copy(board_last)
            board_last = c.copy(board)
            place_sign(board, ai_move_orig, sign)
            n += 1

            steps.append(int(ai_move))

            sign = (sign + 1) % 2

        # Tanulság
        if BREAK == 0:
            if len(steps) > 1:
                sboard = board2str(transform_board(board_last_before)[0], sign)
                forbidden_pos[sboard].add(steps[-2])

            # Van-e olyan kezdő lépés, aminél veszít a másik fél?
            elif len(steps) == 1:
                sboard = board2str(transform_board(board_last)[0], (sign + 1) % 2)
                learning_forbidden_pos[sboard].add(steps[-1])
                print('\nWARNING')
                board_print(board)
                board_print(board_last)
                board_print(board_last_before)
                print(sign)
                print(steps)
                print()

        n_sum += n


    print(forbidden_pos)
    with open('data.txt', 'w') as file:
        for p in forbidden_pos:
            file.write(str(p))
            file.write(str('\n'))
            file.write(str(forbidden_pos[p]))
            file.write(str('\n'))
            file.write(str('\n'))

main()
