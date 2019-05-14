import numpy as np
import time
from collections import defaultdict

from qsy import gates, __version__
from qsy.util import format_complex
from qsy.backends import StatevectorBackend, CHPBackend

from .error import ParseError, QsyASMError
from .parser import QsyASMParser
from .instruction import Operation
from .env import Env
from .log import print_warning, print_info

OPERATION_GATES = {
    Operation.I: gates.I,
    Operation.X: gates.X,
    Operation.Y: gates.Y,
    Operation.Z: gates.Z,

    Operation.H: gates.H,
    Operation.S: gates.S,
    Operation.CX: gates.CX,
    Operation.CY: gates.CY,
    Operation.CZ: gates.CZ,

    Operation.T: gates.T,
    Operation.RX: gates.Rx,
    Operation.RY: gates.Ry,
    Operation.RZ: gates.Rz,
    Operation.CRX: gates.CRx,
    Operation.CRY: gates.CRy,
    Operation.CRZ: gates.CRz,
    Operation.CCX: gates.CCX
}


class QsyASMProgram:
    MAX_PRINTABLE_QUBITS = 16

    def __init__(self, args):
        self.filename = args['filename']

        try:
            with open(self.filename) as f:
                self.input = f.read()
        except FileNotFoundError as e:
            raise QsyASMError('Error reading input: {}'.format(str(e)))

        self.time = args['time']
        self.verbose = args['verbose']
        self.ignore_print_warning = args['ignore_print_warning']
        self.skip_zero_amplitudes = args['skip_zero_amplitudes']

        self.shots = args['shots']
        self.measurement_results = {}

        self.backend_arg = args['backend']
        if self.backend_arg == 'chp':
            self.backend = CHPBackend
        else:
            self.backend = StatevectorBackend

        self._verbose_print('Using {} backend'.format(self.backend.__name__))

        self.parser = QsyASMParser()
        self.env = Env()

    def run(self):
        print_info('qsyasm v{}'.format(__version__))
        print_info('A state vector/stabilizer circuit simulator assembly runner')
        print_info('=' * 60)

        start = time.time()

        try:
            instructions = self.parser.parse(self.input)
        except ParseError as e:
            raise QsyASMError(self._error_message(e.msg, e.lexpos, e.lineno))

        # TODO: we can auto-detect stabilizer circuits and use the CHP back-end
        # when it is capable of printing its state so no features are lost.
        #  if self._can_use_chp(instructions) and self.backend_arg is None:
        #      print_info('Stabilizer circuit detected, using CHP back-end')
        #      self.backend = CHPBackend

        self._verbose_print('Executing {} shots'.format(self.shots))

        for _ in range(self.shots):
            self.eval(instructions)
            self._save_measurements()

        end = time.time()

        self.dump_registers()

        if self.time:
            print_info('Program execution took {:.5f} seconds'.format(end - start))

    def eval(self, instructions):
        for instr in instructions:
            try:
                if instr.is_gate():
                    self._eval_gate(instr)
                elif instr.type == Operation.QR or instr.type == Operation.CR:
                    self._eval_register(instr)
                elif instr.type == Operation.MEASURE:
                    self._eval_measure(instr)
                elif instr.type == Operation.ERROR:
                    raise QsyASMError(
                        self._error_message(
                            'Undefined operation "{}"'.format(instr.op[0]),
                            instr.lexpos,
                            instr.lineno
                        )
                    )
            except QsyASMError as e:
                raise e
            except Exception as e:
                raise QsyASMError(self._error_message(e, instr.lexpos, instr.lineno))

    def dump_registers(self):
        for qr_name, qr in self.env.qrs.items():
            if qr.size > self.MAX_PRINTABLE_QUBITS and not self.ignore_print_warning:
                print_warning(
                    'Quantum register {} too large to print ({} qubits)'.format(
                        qr.name, qr.size) +
                    ' (to print the state anyway, pass ' +
                    '--ignore-print-warning as argument)')
                continue

            print('{}[{}]: {}'.format(qr_name, qr.size, qr.to_dirac()))

            for i, amplitude in qr.yield_state():
                if np.isclose(amplitude, 0) and self.skip_zero_amplitudes:
                    continue

                amplitude = format_complex(amplitude)
                print('{:>8} | {:0{size}b}'.format(amplitude, i, size=qr.size))

        for cr_name, cr in self.env.crs.items():
            if self.shots > 1:
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

        adjoint_message = 'adjoint ' if instr.adjoint else ''
        self._verbose_print('Applying gate {}{} on {}{}'.format(
                            adjoint_message, gate.name, register, targets))

        self.env.qr(register).apply_gate(gate, *targets, adjoint=instr.adjoint)

    def _eval_register(self, instr):
        if len(instr.op) != 2:
            raise QsyASMError(
                self._error_message(
                    'Missing register size in {} definition'.format(instr.op_name),
                    instr.lexpos, instr.lineno
                )
            )

        register_size = instr.op[1]

        if instr.type == Operation.QR:
            for register_name in instr.args:
                self.env.create_qr(register_name, register_size, self.backend)
        elif instr.type == Operation.CR:
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

    def _can_use_chp(self, instructions):
        '''
        Determine if a program is a stabilizer circuit and can use the CHP
        back-end.
        '''
        for instr in instructions:
            if instr.is_gate():
                gate = OPERATION_GATES[instr.type]
                if gate not in CHPBackend.SUPPORTED_GATES:
                    return False

        return True

    def _verbose_print(self, msg):
        if self.verbose:
            print_info(msg)

    def _error_message(self, msg, lexpos, lineno):
        column = self._find_column(lexpos)
        return '{}:{}:{}: {}'.format(self.filename, lineno, column, msg)

    def _find_column(self, lexpos):
        line_start = self.input.rfind('\n', 0, lexpos) + 1
        return (lexpos - line_start) + 1
