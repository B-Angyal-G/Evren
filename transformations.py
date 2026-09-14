import numpy as np

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

mirror = np.zeros((9, 9), dtype='int32')
mirror[0][2] = 1
mirror[1][1] = 1
mirror[2][0] = 1
mirror[3][5] = 1
mirror[4][4] = 1
mirror[5][3] = 1
mirror[6][8] = 1
mirror[7][7] = 1
mirror[8][6] = 1

transformations = np.zeros((8, 9, 9), dtype='int32')
### IDENTITY
transformations[0][0][0] = 1
transformations[0][1][1] = 1
transformations[0][2][2] = 1
transformations[0][3][3] = 1
transformations[0][4][4] = 1
transformations[0][5][5] = 1
transformations[0][6][6] = 1
transformations[0][7][7] = 1
transformations[0][8][8] = 1

### Rotation
transformations[1][0][6] = 1
transformations[1][1][3] = 1
transformations[1][2][0] = 1
transformations[1][3][7] = 1
transformations[1][4][4] = 1
transformations[1][5][1] = 1
transformations[1][6][8] = 1
transformations[1][7][5] = 1
transformations[1][8][2] = 1

transformations[2] = np.dot(transformations[1], transformations[1])
transformations[3] = np.dot(transformations[1], transformations[2])

### Reflection
transformations[4][0][2] = 1
transformations[4][1][1] = 1
transformations[4][2][0] = 1
transformations[4][3][5] = 1
transformations[4][4][4] = 1
transformations[4][5][3] = 1
transformations[4][6][8] = 1
transformations[4][7][7] = 1
transformations[4][8][6] = 1

transformations[5] = np.dot(transformations[1], transformations[4])
transformations[6] = np.dot(transformations[1], transformations[5])
transformations[7] = np.dot(transformations[1], transformations[6])
