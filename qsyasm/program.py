import numpy as np

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
    Operation.CX: gates.C(gates.X),
    Operation.CZ: gates.C(gates.Z),

    Operation.T: gates.T,
    Operation.Tdag: gates.Tdag,
    Operation.RX: gates.Rx,
    Operation.RY: gates.Ry,
    Operation.RZ: gates.Rz,
    Operation.CCX: gates.CC(gates.X)
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
            self.dump_registers()
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

    def dump_registers(self):
        for qr_name, qr in self.env['qrs'].items():
            print('{}[{}]: {} ({})'.format(qr_name, qr.size, qr.state, qr.to_dirac()))

            for i, state in np.ndenumerate(qr.state):
                i = i[0]
                print('  {:>7.5} | {:0{size}b}'.format(state, i, size=qr.size))

        for cr_name, cr in self.env['crs'].items():
            bits = ''.join([str(bit) for bit in cr.state])
            print('{}[{}]: {}'.format(cr_name, cr.size, bits))

    def _eval_gate(self, instr):
        gate = OPERATION_GATES[instr.type]
        args = instr.args

        # TODO: multi qubit gates across registers
        register = args[0][0]
        targets = [arg[1] for arg in args]

        if callable(gate):
            # Parameterized gates like C() or Rz().
            pass

        self.env['qrs'][register].apply_gate(gate, *targets)

    def _eval_qr(self, instr):
        register_size = instr.op[1]

        for register_name in instr.args:
            self.env['qrs'][register_name] = QuantumRegister(register_size)

    def _eval_cr(self, instr):
        register_size = instr.op[1]

        for register_name in instr.args:
            self.env['crs'][register_name] = ClassicalRegister(register_size)

    def _eval_measure(self, instr):
        qtarget = instr.args[0]
        qtarget_name = qtarget[0]

        if len(instr.args) == 2 and len(instr.args[0]) != len(instr.args[1]):
            raise ProgramError(self._error_message(
                instr, 'Mismatched register sizes in measurement'
            ))

        if len(qtarget) == 1:
            # Measure all
            measured = self.env['qrs'][qtarget_name].measure_all()
        elif len(qtarget) == 2:
            # Measure single qubit
            qubit = qtarget[1]
            measured = self.env['qrs'][qtarget_name].measure(qubit)

        if len(instr.args) == 2:
            # Save measurement to classical register
            ctarget = instr.args[1]

            if len(ctarget) == 1:
                if len(qtarget) == 1:
                    # Ensure the classical and quantum registers are of the same size
                    # when measuring all qubits
                    qtarget_size = self.env['qrs'][qtarget].size
                    ctarget_size = self.env['crs'][ctarget].size

                    if qtarget_size != ctarget_size:
                        raise ProgramError(self._error_message(
                            instr,
                            'Mismatched register sizes in measurement ({}[{}] and {}[{}])'.format(
                                qtarget_name, qtarget_size,
                                ctarget[0], ctarget_size
                            )
                        ))

                self.env['crs'][ctarget].set_state(measured)
            elif len(ctarget) == 2:
                register_name, register_index = ctarget
                self.env['crs'][register_name][register_index] = measured

    def _error_message(self, token, msg):
        column = self._find_column(token)
        return '{}:{}:{}: error: {}'.format(self.filename, token.lineno, column, msg)

    def _find_column(self, token):
        line_start = self.input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1
