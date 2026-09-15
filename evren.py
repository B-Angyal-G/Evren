import numpy as np
import copy as c
import random

from transformations import *
from board import *


def ai_preprocess(board, forbiddenpos, sign, n):
    pass



def ai_decision(board_vector, sign):
    choose_list = list()
    for i in range(len(board_vector)):
        if board_vector[i] == 1:
            choose_list.append(i)

    return random.choice(choose_list)


def main():
    # Játéktábla létrehozása
    board = np.array([2, 4, 8, 16, 32, 64, 1, 1, 1])


    # AI-nak átadásra készítés
    ### Keverés
    np.random.shuffle(board)

    print("Kezdő tábla:")
    board_print(board)


    ### Transzformálás
    tran = find_transformation(board)

    print("\nTranszformált (átadott) tábla:")
    tran_board = np.dot(board, transformations[tran])
    board_print(tran_board)
    print("Transzformáció:", tran)

    ai_move = ai_decision(tran_board, 0)
    ai_move_orig = np.argmax(transformations[tran][ai_move:ai_move + 1])    # ai_move-nak megfelelő sorban levő 1-es helye
    print("AI választása a saját nézetéből:", ai_move)
    print("AI választása az eredeti táblán:", ai_move_orig)


    print("\n\nLépés megtétele:")
    place_sign(board, ai_move_orig, 0)
    board_print(board)


main()
