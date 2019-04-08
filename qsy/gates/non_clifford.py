import numpy as np
from .gate import Gate, C, CC
from .pauli import X

T = Gate('T', np.array([[1, 0],
                        [0, np.exp(1j * np.pi / 4)]]), 1)

Tdag = Gate('Tdag', T.matrix.conjugate().transpose(), 1)

def Rx(angle):
    return Gate('Rx', np.array([[np.cos(angle/2), -1j * np.sin(angle/2)],
                                [-1j * np.sin(angle/2), np.cos(angle/2)]]), 1)

def Ry(angle):
    return Gate('Ry', np.array([[np.cos(angle/2), -np.sin(angle/2)],
                                [np.sin(angle/2), np.cos(angle/2)]]), 1)

def Rz(angle):
    return Gate('Rz', np.array([[1, 0],
                                [0, np.exp(1j * angle)]]), 1)

def CRx(angle):
    return C(Rx(angle))

def CRy(angle):
    return C(Ry(angle))

def CRz(angle):
    return C(Rz(angle))

CCX = CC(X)
