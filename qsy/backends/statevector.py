import numpy as np
import numpy.linalg as la
import functools
import itertools

from qsy import gates
from qsy.util import format_complex

from .backend import Backend


class StatevectorBackend(Backend):
    '''
    StatevectorBackend uses a vector to describe the state of the system.
    To evolve the system, vector matrix multiplication is used. It can simulate
    all supported clifford and non-clifford gates.
    '''

    def __init__(self, size, name):
        self.name = name
        self.size = size
        self.state_size = 2**size
        self.state = np.zeros(self.state_size)
        self.state[0] = 1  # Initialize to zero state

    def apply_gate(self, gate, *params, adjoint=False):
        if gate.arity == 1:
            target = params[0]
            self._apply_single_qubit_gate(gate, target, adjoint)
        else:
            *controls, target = params
            self._apply_controlled_gate(gate, controls, target, adjoint)

    def measure_all(self):
        probabilities = np.abs(self.state)**2

        measured = np.random.choice(len(probabilities), p=probabilities)
        self.state[:] = 0
        self.state[measured] = 1

        binary_measurement = format(measured, '0{}b'.format(self.size))
        return [int(x) for x in binary_measurement]

    def measure(self, target):
        step_size = self.state_size // 2**(target+1)
        n_steps = (self.state.size // step_size) // 2

        # Create masks to extract amplitudes where target qubit is zero and one.
        zeros_mask = np.tile(
            np.concatenate((np.ones(step_size), np.zeros(step_size))), n_steps
        )
        ones_mask = np.tile(
            np.concatenate((np.zeros(step_size), np.ones(step_size))), n_steps
        )

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

    def yield_state(self):
        for i, amplitude in np.ndenumerate(self.state):
            yield i[0], amplitude

    def to_dirac(self):
        return ' '.join('{}|{:0{n:d}b}>'.format(format_complex(a), i, n=self.size)
                        for a, i in zip(self.state, itertools.count())
                        if not np.isclose(a, 0.0))

    def _apply_single_qubit_gate(self, gate, target, adjoint):
        self._check_in_range(target)

        operation = gate.adjoint_matrix if adjoint else gate.matrix

        transformation = [gates.I.matrix] * self.size
        transformation[target] = operation

        transformation_matrix = functools.reduce(np.kron, transformation)

        self._transform(transformation_matrix)

    def _apply_controlled_gate(self, gate, controls, target, adjoint):
        self._check_in_range(target)

        for control in controls:
            self._check_in_range(control)

        operation = gate.adjoint_matrix if adjoint else gate.matrix
        control_matrix = np.array([[float('nan'), 0],
                                   [0, 1]])
        transformation = []

        for i in range(self.size):
            if i in controls:
                transformation.append(control_matrix)
            elif i == target:
                transformation.append(operation)
            else:
                transformation.append(gates.I.matrix)

        transformation_matrix = functools.reduce(np.kron, transformation)

        for (i, j), value in np.ndenumerate(transformation_matrix):
            if np.isnan(value):
                if i == j:
                    transformation_matrix[i, j] = 1
                else:
                    transformation_matrix[i, j] = 0

        self._transform(transformation_matrix)

    def _transform(self, operation):
        self.state = np.dot(self.state, operation)

    def _normalize(self):
        self.state = self.state / la.norm(self.state)
