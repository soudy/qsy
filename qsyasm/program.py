from .error import ParseError, ProgramError
from .parser import QsyASMParser
from .instruction import Operation

from qsy import QuantumRegister, ClassicalRegister, gates

OPERATION_GATES = {
    Operation.I: gates.I,
    Operation.X: gates.X,
    Operation.Y: gates.Y,
    Operation.Z: gates.Z,

    Operation.H: gates.H,
    Operation.S: gates.S,
    Operation.Sdag: gates.Sdag,
    Operation.C: gates.C,

    Operation.T: gates.T,
    Operation.Tdag: gates.Tdag,
    Operation.RX: gates.Rx,
    Operation.RY: gates.Ry,
    Operation.RZ: gates.Rz,
    Operation.CC: gates.CC
}

class QsyASMProgram:
    def __init__(self, args):
        self.filename = args['filename']
        self.parser = QsyASMParser()
        self.env = {
            'qrs': {},
            'crs': {},
        }

        try:
            with open(self.filename) as f:
                self.input = f.read()
        except FileNotFoundError as e:
            raise ProgramError('error reading input: {}'.format(str(e)))

    def run(self):
        try:
            instructions = self.parser.parse(self.input)
            self.eval(instructions)
            print(self.env)
        except ParseError as e:
            raise ProgramError(self._error_message(e.token, e.msg))

    def eval(self, instructions):
        for instr in instructions:
            if instr.is_gate():
                self._eval_gate(instr)
            elif instr.type == Operation.QR:
                self._eval_qr(instr)
            elif instr.type == Operation.CR:
                self._eval_cr(instr)
            elif instr.type == Operation.MEASURE:
                self._eval_measure(instr)

    def _eval_gate(self, instr):
        pass

    def _eval_qr(self, instr):
        register_size = instr.op[1]

        for register_name in instr.args:
            self.env['qrs'][register_name] = QuantumRegister(register_size)

    def _eval_cr(self, instr):
        register_size = instr.op[1]

        for register_name in instr.args:
            self.env['crs'][register_name] = ClassicalRegister(register_size)

    def _eval_measure(self, instr):
        target = instr.args[0]
        target_name = target[0]

        if len(instr.args) == 2 and len(instr.args[0]) != len(instr.args[1]):
            raise ProgramError(self._error_message(
                instr, 'Mismatched register sizes in measurement'
            ))

        if len(target) == 1:
            # Measure all
            measured = self.env['qrs'][target_name].measure_all()
        elif len(target) == 2:
            # Measure single qubit
            qubit = target[1]
            measured = self.env['qrs'][target_name].measure(qubit)

        if len(instr.args) == 2:
            # Save measurement to classical register
            classical_target = instr.args[1]

            if len(classical_target) == 1:
                self.env['crs'][classical_target].set_state(measured)
            elif len(classical_target) == 2:
                register_name = classical_target[0]
                register_index = classical_target[1]
                self.env['crs'][register_name][register_index] = measured

    def _error_message(self, token, msg):
        column = self._find_column(token)
        return '{}:{}:{}: error: {}'.format(self.filename, token.lineno, column, msg)

    def _find_column(self, token):
        line_start = self.input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1
