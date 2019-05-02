import itertools
import numpy as np

from .backends import StatevectorBackend, CHPBackend
from .register import Register


class QuantumRegister(Register):
    instance_counter = itertools.count()
    prefix = 'q'

    def __init__(self, size, name=None, backend=StatevectorBackend):
        super().__init__(size, name)
        self.backend = backend(self.size, self.name)

    @property
    def state(self):
        return self.backend.state

    def apply_gate(self, gate, *params, adjoint=False):
        if len(params) != gate.arity:
            raise Exception(
                'Gate {} expects {} parameters, got {}'.format(
                    gate.name, gate.arity, len(params)
                )
            )

        self.backend.apply_gate(gate, *params, adjoint=adjoint)

    def measure_all(self):
        return self.backend.measure_all()

    def measure(self, target):
        return self.backend.measure(target)

    def to_dirac(self):
        return ' '.join('{:+.4f}|{:0{n:d}b}>'.format(a.item(), i, n=self.size)
                        for a, i in zip(self.state, itertools.count())
                        if not np.isclose(a.item(), 0.0))
