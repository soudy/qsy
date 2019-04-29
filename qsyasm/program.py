import numpy as np
import time
from collections import defaultdict

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

    Operation.T: gates.T,
    Operation.Tdag: gates.Tdag,
    Operation.RX: gates.Rx,
    Operation.RY: gates.Ry,
    Operation.RZ: gates.Rz,
    Operation.CRX: gates.CRx,
    Operation.CRY: gates.CRy,
    Operation.CRZ: gates.CRz,
    Operation.CCX: gates.CCX
}


class QsyASMProgram:
    def __init__(self, args):
        self.filename = args['filename']
        self.time = args['time']

        self.shots = args['shots']
        self.measurement_results = {}

        self.parser = QsyASMParser()
        self.env = Env()

        try:
            with open(self.filename) as f:
                self.input = f.read()
        except FileNotFoundError as e:
            raise QsyASMError('Error reading input: {}'.format(str(e)))

    def run(self):
        try:
            start = time.time()
            instructions = self.parser.parse(self.input)
            end = time.time()

            if self.time:
                print('Program execution took {:.5f} seconds'.format(end - start))
        except ParseError as e:
            raise QsyASMError(self._error_message(e.msg, e.lexpos, e.lineno))

        for _ in range(self.shots):
            self.eval(instructions)
            self._save_measurements()

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
                    raise QsyASMError(
                        self._error_message(
                            'Undefined operation "{}"'.format(instr.op[0]), instr
                        )
                    )
            except QsyASMError as e:
                raise QsyASMError(e)
            except Exception as e:
                raise QsyASMError(self._error_message(e, instr.lexpos, instr.lineno))

    def dump_registers(self):
        for qr_name, qr in self.env.qrs.items():
            print('{}[{}]: {}'.format(qr_name, qr.size, qr.to_dirac()))

            for i, amplitude in np.ndenumerate(qr.state):
                amplitude = amplitude if not np.isclose(amplitude, 0.0) else 0.0
                amplitude = '{:9.4f}'.format(amplitude).rstrip('0').rstrip('.')
                i = i[0]
                print('  {} | {:0{size}b}'.format(amplitude, i, size=qr.size))

        for cr_name, cr in self.env.crs.items():
            if cr_name in self.measurement_results:
                bits = dict(self.measurement_results[cr_name])
            else:
                bits = ''.join(str(bit) for bit in cr.state)

            print('{}[{}]: {}'.format(cr_name, cr.size, bits))

    def _eval_gate(self, instr):
        gate = OPERATION_GATES[instr.type]
        args = instr.args

        # TODO: multi qubit gates across registers
        register = args[0][0]
        targets = [arg[1] for arg in args]

        if callable(gate):
            gate_arg = instr.op[1]
            gate = gate(gate_arg)

        self.env.qr(register).apply_gate(gate, *targets)

    def _eval_qr(self, instr):
        register_size = instr.op[1]

        for register_name in instr.args:
            self.env.create_qr(register_name, register_size)

    def _eval_cr(self, instr):
        register_size = instr.op[1]

        for register_name in instr.args:
            self.env.create_cr(register_name, register_size)

    def _eval_measure(self, instr):
        qtarget = instr.args[0]
        qtarget_name = qtarget[0]

        if len(instr.args) == 2 and len(instr.args[0]) != len(instr.args[1]):
            raise QsyASMError(
                self._error_message(
                    'Mismatched register sizes in measurement',
                    instr.lexpos,
                    instr.lineno
                )
            )

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
                        raise QsyASMError(
                            self._error_message(
                                'Mismatched register sizes in measurement ({}[{}] and {}[{}])'.format(
                                    qtarget_name, qtarget_size, ctarget[0], ctarget_size
                                ),
                                instr.lexpos,
                                instr.lineno
                            )
                        )

                self.env.cr(ctarget).set_state(measured)
            elif len(ctarget) == 2:
                ctarget, register_index = ctarget
                self.env.cr(ctarget)[register_index] = measured

        # Save measurement results when shots > 1
        if self.shots > 1 and ctarget not in self.measurement_results:
            self.measurement_results[ctarget] = defaultdict(int)

    def _save_measurements(self):
        for cr_name in self.measurement_results.keys():
            cr_value = self.env.cr(cr_name).state
            bit_string = ''.join(str(bit) for bit in cr_value)
            self.measurement_results[cr_name][bit_string] += 1

    def _error_message(self, msg, lexpos, lineno):
        column = self._find_column(lexpos)
        return '{}:{}:{}: error: {}'.format(self.filename, lineno, column, msg)

    def _find_column(self, lexpos):
        line_start = self.input.rfind('\n', 0, lexpos) + 1
        return (lexpos - line_start) + 1
