class Operation:
    # Gates
    I = 1
    X = 2
    Y = 3
    Z = 4

    H = 5
    S = 6
    Sdag = 7
    C = 8

    T = 9
    Tdag = 10
    RX = 11
    RY = 12
    RZ = 13
    CC = 14

    # Registers
    QR = 15
    CR = 16
)

operations = {
    'i': Operation.I,
    'x': Operation.X,
    'y': Operation.Y,
    'z': Operation.Z,

    'h': Operation.H,
    's': Operation.S,
    'sdag': Operation.Sdag,
    'c': Operation.C,

    't': Operation.T,
    'tdag': Operation.Tdag,
    'rx': Operation.RX,
    'ry': Operation.RY,
    'rz': Operation.RZ,
    'cc': Operation.CC,

    'qreg': Operation.QR,
    'creg': Operation.CR,
}

class Instruction:
    def __init__(self, op_name, args):
        self.op = self._get_op(op_name)
        self.op_name = op
        self.args = args

    def _get_op(self, op):
        if not op in operations:
            raise Exception('Unknown instruction "{}"'.format(op))

        return operations[op]

