import numpy as np

from .error import ParseError, QsyASMError
from .parser import QsyASMParser
from .instruction import Operation
from .env import Env

from qsy import gates

OPERATION_GATES = {
    Operation.I: gates.I,
    Operation.X: gates.X,
    Operation.Y: gates.Y,
    Operation.Z: gates.Z,

    Operation.H: gates.H,
    Operation.S: gates.S,
    Operation.Sdag: gates.Sdag,
    Operation.CX: gates.CX,
    Operation.CY: gates.CY,
    Operation.CZ: gates.CZ,
    Operation.CP: gates.CP,

    Operation.T: gates.T,
    Operation.Tdag: gates.Tdag,
    Operation.RX: gates.Rx,
    Operation.RY: gates.Ry,
    Operation.RZ: gates.Rz,
    Operation.CCX: gates.CCX
}

class QsyASMProgram:
    def __init__(self, args):
        self.filename = args['filename']
        self.parser = QsyASMParser()
        self.env = Env()

        try:
            with open(self.filename) as f:
                self.input = f.read()
        except FileNotFoundError as e:
            raise QsyASMError('Error reading input: {}'.format(str(e)))

    def run(self):
        try:
            instructions = self.parser.parse(self.input)
        except ParseError as e:
            raise QsyASMError(self._error_message(e.token, e.msg))

        self.eval(instructions)
        self.dump_registers()

    def eval(self, instructions):
        for instr in instructions:
            try:
                if instr.is_gate():
                    self._eval_gate(instr)
                elif instr.type == Operation.QR:
                    self._eval_qr(instr)
                elif instr.type == Operation.CR:
                    self._eval_cr(instr)
                elif instr.type == Operation.MEASURE:
                    self._eval_measure(instr)
                elif instr.type == Operation.ERROR:
                    raise QsyASMError(self._error_message(
                        instr, 'Undefined operation "{}"'.format(instr.op[0])))
            except QsyASMError as e:
                raise QsyASMError(e)
            except Exception as e:
                raise QsyASMError(self._error_message(instr, e))

    def dump_registers(self):
        for qr_name, qr in self.env.qrs.items():
            print('{}[{}]: {}'.format(qr_name, qr.size, qr.to_dirac()))

            for i, state in np.ndenumerate(qr.state):
                i = i[0]
                print('  {:>9.5} | {:0{size}b}'.format(state, i, size=qr.size))

        for cr_name, cr in self.env.crs.items():
            bits = ''.join([str(bit) for bit in cr.state])
            print('{}[{}]: {}'.format(cr_name, cr.size, bits))

    def _eval_gate(self, instr):
        gate = OPERATION_GATES[instr.type]
        args = instr.args

        # TODO: multi qubit gates across registers
        register = args[0][0]
        targets = [arg[1] for arg in args]

        if callable(gate):
            gate_arg = instr.op[1][0]
            gate = gate(gate_arg)

        self.env.qr(register).apply_gate(gate, *targets)

    def _eval_qr(self, instr):
        register_size = instr.args[0][1]

        for register_name, _ in instr.args:
            self.env.create_qr(register_name, register_size)

    def _eval_cr(self, instr):
        register_size = instr.args[0][1]

        for register_name, _ in instr.args:
            self.env.create_cr(register_name, register_size)

    def _eval_measure(self, instr):
        qtarget = instr.args[0]
        qtarget_name = qtarget[0]

        if len(instr.args) == 2 and len(instr.args[0]) != len(instr.args[1]):
            raise QsyASMError(self._error_message(
                instr, 'Mismatched register sizes in measurement'
            ))

        if len(qtarget) == 1:
            # Measure all
            measured = self.env.qr(qtarget_name).measure_all()
        elif len(qtarget) == 2:
            # Measure single qubit
            qubit = qtarget[1]
            measured = self.env.qr(qtarget_name).measure(qubit)

        if len(instr.args) == 2:
            # Save measurement to classical register
            ctarget = instr.args[1]

            if len(ctarget) == 1:
                if len(qtarget) == 1:
                    # Ensure the classical and quantum registers are of the same size
                    # when measuring all qubits
                    qtarget_size = self.env.qr(qtarget).size
                    ctarget_size = self.env.cr(ctarget).size

                    if qtarget_size != ctarget_size:
                        raise QsyASMError(self._error_message(
                            instr,
                            'Mismatched register sizes in measurement ({}[{}] and {}[{}])'.format(
                                qtarget_name, qtarget_size,
                                ctarget[0], ctarget_size
                            )
                        ))

                self.env.cr(ctarget).set_state(measured)
            elif len(ctarget) == 2:
                register_name, register_index = ctarget
                self.env.cr(register_name)[register_index] = measured

    def _error_message(self, token, msg):
        column = self._find_column(token)
        return '{}:{}:{}: error: {}'.format(self.filename, token.lineno, column, msg)

    def _find_column(self, token):
        line_start = self.input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1
