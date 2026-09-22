import numpy as np
import copy as c



# <--- Transzformációs mátrixok --->

# Forgatás
rot = np.zeros((9,9), dtype='int32')
rot[0][6] = 1
rot[1][3] = 1
rot[2][0] = 1
rot[3][7] = 1
rot[4][4] = 1
rot[5][1] = 1
rot[6][8] = 1
rot[7][5] = 1
rot[8][2] = 1

# Tükrözés
refl = np.zeros((9, 9), dtype='int32')
refl[0][2] = 1
refl[1][1] = 1
refl[2][0] = 1
refl[3][5] = 1
refl[4][4] = 1
refl[5][3] = 1
refl[6][8] = 1
refl[7][7] = 1
refl[8][6] = 1


# Teljes transzformációs mátrix (8 x 9 x 9)
transformations = np.zeros((8, 9, 9), dtype='int32')

### Identitás
transformations[0][0][0] = 1
transformations[0][1][1] = 1
transformations[0][2][2] = 1
transformations[0][3][3] = 1
transformations[0][4][4] = 1
transformations[0][5][5] = 1
transformations[0][6][6] = 1
transformations[0][7][7] = 1
transformations[0][8][8] = 1

### Forgatások
transformations[1] = np.dot(rot, transformations[0])
transformations[2] = np.dot(rot, transformations[1])
transformations[3] = np.dot(rot, transformations[2])

### Tükrözés -> Forgatások
transformations[4] = np.dot(refl, transformations[0])
transformations[5] = np.dot(rot, transformations[4])
transformations[6] = np.dot(rot, transformations[5])
transformations[7] = np.dot(rot, transformations[6])





# <--- Függvények --->

# Egységes álláshoz szükséges transzformáció megkeresése
def find_transformation(board):
    tmp_board = c.copy(board)
    tmp_matrix = np.reshape(tmp_board, (3, 3))

    # 2x3-as részek összege
    board_forms6_sum = np.array(
        [np.sum(tmp_matrix[:2]),
         np.sum(tmp_matrix[:, 1:3]),
         np.sum(tmp_matrix[1:3]),
         np.sum(tmp_matrix[:, :2])],
        dtype = 'int32'
    )

    # 2x2-es sarkok összege
    board_forms4_sum = np.array(
        [np.sum(tmp_matrix[:2][:, :2]),
         np.sum(tmp_matrix[:2][:, 1:]),
         np.sum(tmp_matrix[1:][:, 1:]),
         np.sum(tmp_matrix[1:][:, :2])],
        dtype = 'int32'
    )

    # 2x3-asok maximum elemeinek indexei
    idx_max6 = np.flatnonzero(board_forms6_sum == board_forms6_sum.max())
    index_max6 = idx_max6[0]

    # Ha csak egy max 2x3-as rész van
    if idx_max6.size == 1:
        if board_forms4_sum[index_max6] > board_forms4_sum[(index_max6 + 1) % 4]:
            return index_max6
        else:
            return index_max6 + 4

    else:
        index_max4 = np.argmax(board_forms4_sum)

        match index_max4:
            case 0:
                if board[1] >= board[3]:
                    return 0
                return 7
            case 1:
                if board[5] >= board[1]:
                    return 1
                return 4
            case 2:
                if board[7] >= board[5]:
                    return 2
                return 5
            case 3:
                if board[3] >= board[7]:
                    return 3
                return 6


# Tábla forgatása egységes állásra, transzformáció visszaadása is
def transform_board(board):
    tmp_board = c.copy(board)
    t = find_transformation(board)

    return (np.dot(tmp_board, transformations[t]), t)
