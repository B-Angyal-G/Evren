import numpy as np
import copy as c
import time as t
import random
import matplotlib.pyplot as plt

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
    # Nyerő lépés
    force_win = if_force_win(board, 0)
    if force_win != -1:
        return (force_win, 0)

    # Egyébként
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
        return (random.choice(choose_list), len(choose_list))
    else:
        return (-1, len(choose_list))



def main():
    # Működési paraméterek inicializálása
    MAX_GAME = 100000       # Max játék lejátszás
    STEP_INTERVAL = 200     # Adatgyűjtéshez lépésköz
    BREAK_LIMIT = 1000      # Jaték megszakításának lépéshatára
    LEARN = 1               # Legyen-e tanítás TODO: JÁTÉKMÓD ELKÉSZÍTÉSE

    # Statisztikához változók, listák
    game_start = t.time()       # Folyamat indításának ideje
    step_nums = list()          # Lépésközben megtett összes lépés
    possibility_nums = list()   # Adott lépésközben összes választási lehetőség összege
    possibility_ratio = list()  # Adott lépésközben választási lehetőségek és összes lépés aránya
    breaks = list()             # Adott lépésközben megszakítások száma
    interval_times = list()     # Lépésközben eltelt idő
    abs_time = list()           # Adott lépésköz végéig eltelt idő a kezdetektől

    time_start = t.time()
    br = 0
    step_sum = 0
    possibility_sum = 0

    # Működéshez szükséges adatszerkezetek
    forbidden_pos = defaultdict(set)
    learning_forbidden_pos = defaultdict(set)

    for i in range(MAX_GAME):
        board = np.ones(9, dtype='int32')
        board_prev = np.ones(9, dtype='int32')
        board_prev_prev = np.ones(9, dtype='int32')

        steps = list()

        sign = 0
        BREAK = 0

        # Statisztikai adatok felvétele
        if i % STEP_INTERVAL == 0:
            print(i)
            interval_time = t.time() - time_start
            ratio = possibility_sum/(step_sum + 1)

            # Listákhoz adás
            interval_times.append(interval_time)
            abs_time.append(t.time() - game_start)
            step_nums.append(step_sum)
            possibility_nums.append(possibility_sum)
            possibility_ratio.append(ratio)
            breaks.append(br)

            # Kiíratás
            print("Intervallum idő:", interval_time)
            print('Lépések száma:', step_sum)
            print('Összes lehetséges választás száma:',  possibility_sum)
            print('Arány:', ratio)
            print('Break szám:', br)
            print()
            
            # Nullázás
            br = 0
            step_sum = 0
            possibility_sum = 0
            time_start = t.time()



        n = 0
        while if_game_end(board) == -1:
            if n == BREAK_LIMIT:
                BREAK = 1
                br += 1
                break

            # Tábla transzformálása egységes alakra
            transformed_board, tran = transform_board(board)

            # AI-nak átadás
            ai_move, ai_possibility = ai_decision(transformed_board, forbidden_pos, sign, n, LEARN, learning_forbidden_pos)

            # Hány hely közül választott
            possibility_sum += ai_possibility


            # Ha az AI nem tud lépni, mert minden érvényes helyet már tiltólistára tett
            if ai_move == -1:
                break

            # Eredeti táblának megfelelő lépés helye
            ai_move_orig = np.argmax(transformations[tran][:, ai_move:ai_move + 1])    # ai_move-nak megfelelő oszlopban levő 1-es helye

            # Utolsó két állás nyomon követése
            board_prev_prev = c.copy(board_prev)
            board_prev = c.copy(board)

            # Lépés megtétele
            place_sign(board, ai_move_orig, sign)
            n += 1

            steps.append(int(ai_move))

            sign = (sign + 1) % 2

        # Tanulság, ha nem lett leállítva a játék túl sok lépés miatt
        if BREAK == 0:
            if len(steps) > 1:
                sboard = board2str(transform_board(board_prev_prev)[0], sign)   # Emiatt nem lehet a transzformációt ai_decision-ba beépíteni
                forbidden_pos[sboard].add(steps[-2])

            # Van-e olyan kezdő lépés, aminél veszít a másik fél?
            elif len(steps) == 1:
                sboard = board2str(transform_board(board_prev)[0], (sign + 1) % 2)
                learning_forbidden_pos[sboard].add(steps[-1])
                print('\nWARNING')
                board_print(board)
                board_print(board_prev)
                board_print(board_prev_prev)
                print(sign)
                print(steps)
                print()

        step_sum += n


    # Megtanult tiltott lépések file-ba írása
    with open('data.txt', 'w') as file:
        for p in forbidden_pos:
            file.write(str(p))
            file.write(str('\n'))
            for num in forbidden_pos[p]:
                file.write(str(num))
            file.write(str('\n'))

    # Statisztikai adatok file-ba írása
    with open('statistic.txt', 'w') as file:
        # Fejléc
        file.write(str('#'))
        file.write(str('Interval\t'))   # Adatösszegzéshez lépésköz
        file.write(str('Step nums\t'))  # Lépésközben megtett összes lépés
        file.write(str('Times\t'))      # Lépésközben eltelt idő
        file.write(str('Abs time\t'))   # Adott lépésköz végéig eltelt idő a kezdetektől
        file.write(str('Breaks\t'))     # Adott lépésközben megszakítások száma
        file.write(str('Pos nums\t'))   # Adott lépésközben összes választási lehetőség összege
        file.write(str('Pos ratio'))    # Adott lépésközben választási lehetőségek és összes lépés aránya
        file.write(str('\n'))

        # Adatok
        for i in range(1, len(interval_times)):
            file.write(str(STEP_INTERVAL * i))
            file.write(str('\t'))
            file.write(str(step_nums[i]))
            file.write(str('\t'))
            file.write(str(interval_times[i]))
            file.write(str('\t'))
            file.write(str(abs_time[i]))
            file.write(str('\t'))
            file.write(str(breaks[i]))
            file.write(str('\t'))
            file.write(str(possibility_nums[i]))
            file.write(str('\t'))
            file.write(str(possibility_ratio[i]))
            file.write(str('\n'))
    print("Futási idő:", t.time() - game_start)

    # Adatok ábrázolása
    x_axis = [STEP_INTERVAL * i for i in range(len(abs_time))]

    plt.plot(x_axis, possibility_ratio)
    plt.show()


main()
