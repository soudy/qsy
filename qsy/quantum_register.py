import itertools
import numpy as np
from .register import Register
from .qubit_state import QubitState

class QuantumRegister(Register):
    def __init__(self, size):
        super().__init__(size)
        self.state = QubitState(size)

    def apply_gate(self, gate, *params):
        if len(params) != gate.arity:
            raise Exception('Gate {} expects {} parameters'.format(gate.name,
                gate.arity))

        if gate.arity == 1:
            target = params[0]
            self.state.apply_single_qubit_gate(gate, target)
        else:
            *controls, target = params
            self.state.apply_multi_qubit_gate(gate, controls, target)

    def measure_all(self):
        return self.state.measure_all()

    def measure(self, target, classical_target=None):
        measurement = self.state.measure(target)

        if classical_target is not None:
            print(classical_target)

        return measurement

    def to_dirac(self):
        return ' '.join('{:+.4f}|{:0{n:d}b}>'.format(a.item(), i, n=self.size)
                          for a, i in zip(self.state.statevector, itertools.count())
                          if not np.isclose(a.item(), 0.0))
