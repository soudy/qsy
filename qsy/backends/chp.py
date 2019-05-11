import numpy as np

from qsy import gates
from qsyasm.log import print_info

from .backend import Backend


class CHPBackend(Backend):
    '''
    CHPBackend can efficiently simulate stabilizer circuits (circuits consisting
    of only CNOT, H and phase gates). The algorithm used to achieve this is
    described in a paper by Scott Aaronson and Daniel Gottesman found at
    https://arxiv.org/abs/quant-ph/0406196.
    '''

    SUPPORTED_GATES = [gates.CX, gates.H, gates.S, gates.X, gates.Z, gates.CZ]

    def __init__(self, size, name):
        self.name = name
        self.size = size

        # Initialize tableau
        # X generators
        self.x = np.concatenate(
            (np.eye(self.size, dtype=np.int8),
             np.zeros((self.size, self.size), dtype=np.int8),
             # scratch space
             np.zeros((1, self.size), dtype=np.int8)),
            axis=0
        )

        # Z generators
        self.z = np.concatenate(
            (np.zeros((self.size, self.size), dtype=np.int8),
             np.eye(self.size, dtype=np.int8),
             # scratch space
             np.zeros((1, self.size), dtype=np.int8)),
            axis=0
        )

        # Phase (0 for +1, 1 for i, 2 for -1, 3 for -i)
        self.r = np.zeros((2*self.size + 1, 1), dtype=np.int8)

    def apply_gate(self, gate, *params, adjoint=False):
        if gate not in self.SUPPORTED_GATES:
            supported_gate_names = map(lambda g: g.name, self.SUPPORTED_GATES)
            raise Exception(
                'Unsupported gate "{}" for CHP back-end. '.format(gate.name) +
                'Supported gates are {}.'.format(', '.join(supported_gate_names))
            )

        if gate.arity == 1:
            target = params[0]
        else:
            control, target = params

            self._check_in_range(control)

        self._check_in_range(target)

        if gate == gates.CX:
            self._cnot(control, target)
        elif gate == gates.H:
            self._h(target)
        elif gate == gates.S:
            if adjoint:
                # S^dagger = SSS
                self._s(target)
                self._s(target)

            self._s(target)
        elif gate == gates.X:
            self._x(target)
        elif gate == gates.Z:
            self._z(target)
        elif gate == gates.CZ:
            self._cz(control, target)

    def measure(self, target):
        p = None
        for i in range(self.size, 2*self.size):
            if self.x[i, target] == 1:
                p = i
                break

        if p is not None:
            # Measurement outcome is probabilistic
            for i in range(2*self.size):
                if i != p and self.x[i, target] == 1:
                    self._rowsum(i, p)

            # Set (p−n)th row equal to pth row
            self.x[p-self.size] = self.x[p]
            self.z[p-self.size] = self.z[p]
            self.r[p-self.size] = self.r[p]

            self.x[p] = 0
            self.z[p] = 0

            measurement = np.random.randint(2)
            self.r[p] = measurement

            self.z[p, target] = 1

            return measurement
        else:
            # Measurement outcome is deterministic
            self.x[2*self.size] = 0
            self.z[2*self.size] = 0
            self.r[2*self.size] = 0

            for i in range(self.size):
                if self.x[i, target] == 1:
                    self._rowsum(2*self.size, i + self.size)

            return int(self.r[2*self.size])

    def measure_all(self):
        return [self.measure(i) for i in range(self.size)]

    def yield_state(self):
        print_info(
            'Printing quantum state is not supported by the CHP back-end. ' +
            'Use the statevector back-end if you wish to see the quantum state.'
        )
        yield from []

    def to_dirac(self):
        # TODO: make CHP state printable/readable
        return ''

    def _h(self, target):
        for i in range(2*self.size):
            self.r[i] ^= self.x[i, target] & self.z[i, target]
            self.x[i, target], self.z[i, target] = self.z[i, target], self.x[i, target]

    def _cnot(self, control, target):
        for i in range(2*self.size):
            self.r[i] ^= self.x[i, control] & self.z[i, target]
            self.r[i] &= self.x[i, target] ^ self.z[i, control] ^ 1

            self.x[i, target] ^= self.x[i, control]
            self.z[i, control] ^= self.z[i, target]

    def _s(self, target):
        for i in range(2*self.size):
            self.r[i] ^= self.x[i, target] & self.z[i, target]
            self.z[i, target] ^= self.x[i, target]

    def _x(self, target):
        self._h(target)
        self._z(target)
        self._h(target)

    def _z(self, target):
        self._s(target)
        self._s(target)

    def _cz(self, control, target):
        self._h(target)
        self._cnot(control, target)
        self._h(target)

    def _rowsum(self, h, i):
        '''
        Set generator h equal to h + i. Keep track of the factors of i that r_h
        goes through when multiplying Pauli matrices.
        '''
        def g(x1, z1, x2, z2):
            '''
            Return the exponent to which i is raised (either 0, 1, or −1) when
            the Pauli matrices represented by x1 z1 and x2 z2 are multiplied.
            '''
            if x1 == z1 == 0:
                return 0
            if x1 == z1 == 1:
                return z2 - x2
            if x1 == 1 and z1 == 0:
                return z2 * (2*x2 - 1)
            if x1 == 0 and z1 == 1:
                return x2 * (1 - 2*z2)

        rowsum = sum(g(self.x[i, j], self.z[i, j], self.x[h, j], self.z[h, j])
                     for j in range(self.size))
        rowsum += 2*self.r[h] + 2*self.r[i]

        if rowsum == 0:
            self.r[h] = 0
        elif rowsum == 2 % 4:
            self.r[h] = 1

        for j in range(self.size):
            self.x[h, j] ^= self.x[i, j]
            self.z[h, j] ^= self.z[i, j]
