import numpy as np
import copy as c
import random

import transformations as t
from board import *


def find_transformation(board_vector):
    tmp_vector = c.copy(board_vector)
    tmp_matrix = np.reshape(tmp_vector, (3, 3))

    board_forms6_sum = np.array(
        [np.sum(tmp_matrix[:2]),
         np.sum(tmp_matrix[:, 1:3]),
         np.sum(tmp_matrix[1:3]),
         np.sum(tmp_matrix[:, :2])],
        dtype = 'int32'
    )

    board_forms4_sum = np.array(
        [np.sum(tmp_matrix[:2][:, :2]),
         np.sum(tmp_matrix[:2][:, 1:]),
         np.sum(tmp_matrix[1:][:, 1:]),
         np.sum(tmp_matrix[1:][:, :2])],
        dtype = 'int32'
    )

    index_max = np.argmax(board_forms6_sum)

    # print("\n\nIn find_transformation:")
    # print(board_forms6_sum)
    # print(board_forms4_sum)
    # print(index_max)
    # print("\n\n")

    if board_forms4_sum[index_max] == board_forms4_sum[(index_max + 1) % 4]:
        print('EGYENLŐSÉG!!!\n', board_vector)

    if board_forms4_sum[index_max] > board_forms4_sum[(index_max + 1) % 4]:
        return 2 * index_max
    else:
        return 2 * index_max + 1

def ai_decision(board_vector):
    choose_list = list()
    for i in range(len(board_vector)):
        if board_vector[i] == 0:
            choose_list.append(i)

    return random.choice(choose_list)


def main():
    # b = np.array([2, 64, 0, 8, 0, 0, 4, 32, 16])
    #
    # board_print(b)
    # print(find_transformation(b))
    #
    # return 0

    # Játéktábla létrehozása
    board = np.arange(1, 7, 1)
    board = np.array([2, 4, 8, 16, 32, 64, 0, 0, 0
    board = np.concatenate( ( board, np.array([0, 0, 0]) ) )


    # AI-nak átadásra készítés
    ### Keverés
    np.random.shuffle(board)


    ### 2 Hatványozás
    power_of_2 = lambda x: np.where(x > 0, 2**x, 0)
    numerical_board = power_of_2(board)

    print("Kezdő tábla:")
    board_print(board)
    print()
    board_print(numerical_board)


    ### Transzformálás
    tran = find_transformation(numerical_board)

    print("\nTranszformált (átadott) tábla:")
    tran_board = np.dot(t.transformations[tran], board)
    board_print(tran_board)
    print("Transzformáció:", tran)

    ai_move = ai_decision(tran_board)
    ai_move_orig = np.argmax(t.transformations[tran][ai_move:ai_move + 1]) # ai_move-nak megfelelő sorban levő 1-es helye
    print("AI választása a saját nézetéből:", ai_move)
    print("AI választása az eredeti táblán:", ai_move_orig)


    print("\n\nLépés megtétele:")
    place_sign(board, ai_move_orig, 0)
    board_print(board)


main()
