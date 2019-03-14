import numpy as np
from .gate import Gate

H = Gate('H', 1/np.sqrt(2) * np.array([[1,  1],
                                       [1, -1]]), 1)

S = Gate('S', np.array([[1, 0],
                        [0, 1j]]), 1)

Sdag = Gate('Sd', S.matrix.conjugate().transpose(), 1)

def C(gate):
    """Create a controlled-U gate."""
    return Gate('C{}'.format(gate.name), gate.matrix, 2)
