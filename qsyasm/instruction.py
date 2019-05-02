from enum import Enum
from .error import QsyASMError


class Operation:
    # Gates
    GATES_START = 0
    I = 1
    X = 2
    Y = 3
    Z = 4

    H = 5
    S = 6
    CX = 7
    CY = 8
    CZ = 9

    T = 10
    RX = 11
    RY = 12
    RZ = 13
    CRX = 14
    CRY = 15
    CRZ = 16
    CCX = 17
    GATES_END = 18

    # Registers
    QR = 19
    CR = 20

    MEASURE = 21

    ERROR = 22


operations = {
    'i': Operation.I,
    'x': Operation.X,
    'y': Operation.Y,
    'z': Operation.Z,

    'h': Operation.H,
    's': Operation.S,
    'cx': Operation.CX,
    'cz': Operation.CZ,

    't': Operation.T,
    'rx': Operation.RX,
    'ry': Operation.RY,
    'rz': Operation.RZ,
    'crx': Operation.CRX,
    'cry': Operation.CRY,
    'crz': Operation.CRZ,
    'ccx': Operation.CCX,

    'qreg': Operation.QR,
    'creg': Operation.CR,

    'meas': Operation.MEASURE,

    'error': Operation.ERROR
}


class Instruction:
    def __init__(self, op, args, lineno, lexpos):
        self.op = op
        self.op_name = op
        self.args = args
        self.lineno = lineno
        self.lexpos = lexpos

        self.type = self._get_op_type()

        # only applicable for gates
        self.adjoint = False

    def is_gate(self):
        return self.type > Operation.GATES_START and self.type < Operation.GATES_END

    def toggle_adjoint(self):
        self.adjoint = not self.adjoint

    def _get_op_type(self):
        self.op_name = self.op

        if isinstance(self.op, tuple):
            # parameterized instruction like qreg[n] or c(x)
            self.op_name, _ = self.op

        if self.op_name not in operations:
            return Operation.ERROR

        return operations[self.op_name]

    def __repr__(self):
        return '{}<{} {}>'.format(self.__class__.__name__, self.op, self.args)
