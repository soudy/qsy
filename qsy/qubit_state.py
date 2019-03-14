import functools
import numpy as np
import numpy.linalg as la
from . import gates

class QubitState:
    def __init__(self, n):
        self.size = n
        self.state_size = 2**n
        self.statevector = np.zeros(self.state_size)
        self.statevector[0] = 1 # Initialize to zero state

    def apply_single_qubit_gate(self, gate, target):
        self._check_in_range(target)

        transformation = [gates.I.matrix] * self.size
        transformation[target] = gate.matrix

        transformation_matrix = functools.reduce(np.kron, transformation)

        self._transform(transformation_matrix)

    def apply_multi_qubit_gate(self, gate, controls, target):
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

    def measure_all(self):
        probabilities = np.abs(self.statevector)**2

        measured = np.random.choice(len(probabilities), p=probabilities)
        self.statevector[:] = 0
        self.statevector[measured] = 1

    def measure(self, target):
        self._check_in_range(target)

        step_size = self.state_size // 2**(target+1)
        n_steps = (self.statevector.size // step_size) // 2

        # Create masks to extract amplitudes where target qubit is zero and one.
        zeros_mask = np.tile(np.concatenate((np.ones(step_size), np.zeros(step_size))),
                             n_steps)
        ones_mask = np.tile(np.concatenate((np.zeros(step_size), np.ones(step_size))),
                            n_steps)

        zero_amplitudes = self.statevector * zeros_mask
        one_amplitudes = self.statevector * ones_mask
        probabilities = np.abs(zero_amplitudes + one_amplitudes)**2

        measured = np.random.choice(len(probabilities), p=probabilities)
        measured_value = 1 if one_amplitudes[measured] != 0.0 else 0

        if measured_value == 1:
            for i in zero_amplitudes.nonzero():
                self.statevector[i] = 0
        else:
            for i in one_amplitudes.nonzero():
                self.statevector[i] = 0

        self._normalize()

        return measured_value

    def _transform(self, operation):
        self.statevector = np.dot(self.statevector, operation)

    def _normalize(self):
        self.statevector = self.statevector / la.norm(self.statevector)

    def _check_in_range(self, target):
        if target < 0 or target >= self.size:
            raise Exception('Can\'t access qubit {}: register index out of' +
                    'range (state size {})'.format(target, self.size))
