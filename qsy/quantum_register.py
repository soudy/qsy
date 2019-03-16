import itertools
import functools
import numpy as np
import numpy.linalg as la

from .register import Register
from . import gates

class QuantumRegister(Register):
    def __init__(self, size):
        super().__init__(size)
        self.state_size = 2**size
        self.state = np.zeros(self.state_size)
        self.state[0] = 1 # Initialize to zero state

    def apply_gate(self, gate, *params):
        if len(params) != gate.arity:
            raise Exception('Gate {} expects {} parameters'.format(gate.name,
                gate.arity))

        if gate.arity == 1:
            target = params[0]
            self._apply_single_qubit_gate(gate, target)
        else:
            *controls, target = params
            self._apply_multi_qubit_gate(gate, controls, target)

    def measure_all(self):
        probabilities = np.abs(self.state)**2

        measured = np.random.choice(len(probabilities), p=probabilities)
        self.state[:] = 0
        self.state[measured] = 1

    def measure(self, target):
        self._check_in_range(target)

        step_size = self.state_size // 2**(target+1)
        n_steps = (self.state.size // step_size) // 2

        # Create masks to extract amplitudes where target qubit is zero and one.
        zeros_mask = np.tile(np.concatenate((np.ones(step_size), np.zeros(step_size))),
                             n_steps)
        ones_mask = np.tile(np.concatenate((np.zeros(step_size), np.ones(step_size))),
                            n_steps)

        zero_amplitudes = self.state * zeros_mask
        one_amplitudes = self.state * ones_mask
        probabilities = np.abs(zero_amplitudes + one_amplitudes)**2

        measured = np.random.choice(len(probabilities), p=probabilities)
        measured_value = 1 if one_amplitudes[measured] != 0.0 else 0

        if measured_value == 1:
            for i in zero_amplitudes.nonzero():
                self.state[i] = 0
        else:
            for i in one_amplitudes.nonzero():
                self.state[i] = 0

        self._normalize()

        return measured_value

    def _apply_single_qubit_gate(self, gate, target):
        self._check_in_range(target)

        transformation = [gates.I.matrix] * self.size
        transformation[target] = gate.matrix

        transformation_matrix = functools.reduce(np.kron, transformation)

        self._transform(transformation_matrix)

    def _apply_multi_qubit_gate(self, gate, controls, target):
        self._check_in_range(target)

        for control in controls:
            self._check_in_range(control)

        control_matrix = np.array([[float('nan'), 0],
                                   [0, 1]])
        transformation = []

        for i in range(self.size):
            if i in controls:
                transformation.append(control_matrix)
            elif i == target:
                transformation.append(gate.matrix)
            else:
                transformation.append(gates.I.matrix)

        transformation_matrix = functools.reduce(np.kron, transformation)

        for (i, j), value in np.ndenumerate(transformation_matrix):
            if np.isnan(value):
                if i == j:
                    transformation_matrix[i][j] = 1
                else:
                    transformation_matrix[i][j] = 0

        self._transform(transformation_matrix)

    def _transform(self, operation):
        self.state = np.dot(self.state, operation)

    def _normalize(self):
        self.state = self.state / la.norm(self.state)

    def _check_in_range(self, target):
        if target < 0 or target >= self.size:
            raise Exception('Can\'t access qubit {}: register index out of' +
                    'range (register size {})'.format(target, self.size))

    def to_dirac(self):
        return ' '.join('{:+.4f}|{:0{n:d}b}>'.format(a.item(), i, n=self.size)
                          for a, i in zip(self.state, itertools.count())
                          if not np.isclose(a.item(), 0.0))
