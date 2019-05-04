import itertools

from .backends import StatevectorBackend
from .register import Register


class QuantumRegister(Register):
    instance_counter = itertools.count()
    prefix = 'q'

    def __init__(self, size, name=None, backend=StatevectorBackend):
        super().__init__(size, name)
        self.backend = backend(self.size, self.name)

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

    def yield_state(self):
        return self.backend.yield_state()

    def to_dirac(self):
        return self.backend.to_dirac()
