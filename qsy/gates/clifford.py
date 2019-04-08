import numpy as np
from .gate import Gate, C
from .pauli import X, Y, Z

H = Gate('H', 1/np.sqrt(2) * np.array([[1,  1],
                                       [1, -1]]), 1)

S = Gate('S', np.array([[1, 0],
                        [0, 1j]]), 1)

Sdag = Gate('Sdag', S.matrix.conjugate().transpose(), 1)

CX = C(X)
CY = C(Y)
CZ = C(Z)
