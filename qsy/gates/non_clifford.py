import numpy as np
from .gate import Gate, C, CC
from .pauli import X

T_MATRIX = np.array([[1, 0],
                     [0, np.exp(1j * np.pi / 4)]])

T = Gate('T', T_MATRIX, T_MATRIX.conj().T, 1)


def Rx(angle):
    matrix = np.array([[np.cos(angle/2), -1j * np.sin(angle/2)],
                       [-1j * np.sin(angle/2), np.cos(angle/2)]])
    return Gate('Rx', matrix, matrix.conj().T, 1)


def Ry(angle):
    matrix = np.array([[np.cos(angle/2), -np.sin(angle/2)],
                       [np.sin(angle/2), np.cos(angle/2)]])
    return Gate('Ry', matrix, matrix.conj().T, 1)


def Rz(angle):
    matrix = np.array([[1, 0],
                       [0, np.exp(1j * angle)]])
    return Gate('Rz', matrix, matrix.conj().T, 1)


def CRx(angle):
    return C(Rx(angle))


def CRy(angle):
    return C(Ry(angle))


def CRz(angle):
    return C(Rz(angle))


CCX = CC(X)
