import numpy as np
from .gate import Gate

I = Gate('I', np.array([[1, 0],
                        [0, 1]]), 1)

X = Gate('X', np.array([[0, 1],
                        [1, 0]]), 1)

Y = Gate('Y', np.array([[0, -1j],
                        [1j, 0]]), 1)

Z = Gate('Z', np.array([[1,  0],
                        [0, -1]]), 1)
