from enum import IntEnum, auto, unique
from .error import QsyASMError


@unique
class Operation(IntEnum):
    # Gates
    GATES_START = auto()
    I = auto()
    X = auto()
    Y = auto()
    Z = auto()

    H = auto()
    S = auto()
    CX = auto()
    CY = auto()
    CZ = auto()

    T = auto()
    RX = auto()
    RY = auto()
    RZ = auto()
    CRX = auto()
    CRY = auto()
    CRZ = auto()
    CCX = auto()
    GATES_END = auto()

    # Registers
    QR = auto()
    CR = auto()

    MEASURE = auto()

    ERROR = auto()


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
