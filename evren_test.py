import os
import numpy as np
import copy as c
import random
from collections import defaultdict

from transformations import *
from board import *

def clrscr():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    board = np.array([2, 4, 8, 16, 32, 64, 0, 0, 0])
    # board = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

    np.random.shuffle(board)
    board_print(board)
    print()
    board_print_sign(list(board))
    print()
    game = if_game_end(board)
    if game == 0 or game == 1:
        board_print_sign(list(board))
        print(game)
        print('\n')

    return 0
    for _ in range(10):
        np.random.shuffle(board)
        game = if_game_end(board)
        if game == 0 or game == 1:
            board_print_sign(list(board))
            print('\n')

    return 0

    # TRANSZFORMÁCIÓK MŰKÖDÉSÉNEK ELLENŐRZÉSE
    board = np.array([2,4,0,0,0,0,0,0,0])

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
        print(s,d[s])

    sign = 0
    board = np.array([32,64,0,16,2,4,0,8,0], dtype='int32')
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
    board = np.array([32,64,0,16,2,4,0,8,0], dtype='int32')

    print(board)
    sboard = board2str(board)
    print(sboard)
    print(str2board(sboard))
    return 0
    while ch!= 'q' and ch != 'Q':
        board_print(board)
        print(sign)
        print(s)
        print(board)
        print(np.append(board, sign))
        ch = input()
        if ch == 'r' or ch == 'R':
            s= 0
            clrscr()
            continue
        pos = int(ch)
        s += 1
        place_sign(board, pos, sign)
        sign = (sign + 1) % 2
        clrscr()


main()
