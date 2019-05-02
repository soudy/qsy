import numpy as np
from .gate import Gate, C
from .pauli import X, Y, Z

H_MATRIX = 1/np.sqrt(2) * np.array([[1,  1],
                                    [1, -1]])
S_MATRIX = np.array([[1, 0],
                     [0, 1j]])

H = Gate('H', H_MATRIX, H_MATRIX, 1)

S = Gate('S', S_MATRIX, S_MATRIX.conj().T, 1)

CX = C(X)
CY = C(Y)
CZ = C(Z)
