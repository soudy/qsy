import numpy as np
from .gate import Gate
from .pauli import X, Y, Z

H = Gate('H', 1/np.sqrt(2) * np.array([[1,  1],
                                       [1, -1]]), 1)

S = Gate('S', np.array([[1, 0],
                        [0, 1j]]), 1)

Sdag = Gate('Sdag', S.matrix.conjugate().transpose(), 1)

def P(angle):
    return Gate('P', np.array([[1, 0],
                               [0, np.exp(1j * angle)]]), 1)

def C(gate):
    """Create a controlled-U gate."""
    return Gate('C{}'.format(gate.name), gate.matrix, 2)

CX = C(X)
CY = C(Y)
CZ = C(Z)

def CP(angle):
    return C(P(angle))
