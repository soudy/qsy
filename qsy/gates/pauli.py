import numpy as np
from .gate import Gate

PAULI_I_MATRIX = np.array([[1, 0],
                           [0, 1]])
PAULI_X_MATRIX = np.array([[0, 1],
                           [1, 0]])
PAULI_Y_MATRIX = np.array([[0, -1j],
                           [1j, 0]])
PAULI_Z_MATRIX = np.array([[1,  0],
                           [0, -1]])

I = Gate('I', PAULI_I_MATRIX, PAULI_I_MATRIX, 1)

X = Gate('X', PAULI_X_MATRIX, PAULI_X_MATRIX, 1)

Y = Gate('Y', PAULI_Y_MATRIX, PAULI_Y_MATRIX, 1)

Z = Gate('Z', PAULI_Z_MATRIX, PAULI_Z_MATRIX, 1)
