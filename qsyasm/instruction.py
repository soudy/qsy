from .error import ParseError

class Operation:
    # Gates
    GATES_START = 0
    I = 1
    X = 2
    Y = 3
    Z = 4

    H = 5
    S = 6
    Sdag = 7
    CX = 8
    CY = 9
    CZ = 10

    T = 11
    Tdag = 12
    RX = 13
    RY = 14
    RZ = 15
    CRX = 16
    CRY = 17
    CRZ = 18
    CCX = 19
    GATES_END = 20

    # Registers
    QR = 21
    CR = 22

    MEASURE = 23

operations = {
    'i': Operation.I,
    'x': Operation.X,
    'y': Operation.Y,
    'z': Operation.Z,

    'h': Operation.H,
    's': Operation.S,
    'sdag': Operation.Sdag,
    'cx': Operation.CX,
    'cz': Operation.CZ,

    't': Operation.T,
    'tdag': Operation.Tdag,
    'rx': Operation.RX,
    'ry': Operation.RY,
    'rz': Operation.RZ,
    'crx': Operation.CRX,
    'cry': Operation.CRY,
    'crz': Operation.CRZ,
    'ccx': Operation.CCX,

    'qreg': Operation.QR,
    'creg': Operation.CR,

    'meas': Operation.MEASURE
}

class Instruction:
    def __init__(self, op, args, lineno, lexpos):
        self.op = op
        self.args = args
        self.lineno = lineno
        self.lexpos = lexpos
        self.type = self._get_op_type()

    def is_gate(self):
        return self.type > Operation.GATES_START and self.type < Operation.GATES_END

    def _get_op_type(self):
        op_name = self.op

        if isinstance(self.op, tuple):
            # parameterized instruction like qreg[n] or c(x)
            op_name, _ = self.op

        if not op_name in operations:
            raise ParseError('Unknown instruction \'{}\''.format(op_name), self.token)

        return operations[op_name]

    def __repr__(self):
        return '{}<{} {}>'.format(self.__class__.__name__, self.op, self.args)
