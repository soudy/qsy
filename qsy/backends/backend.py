import abc


class Backend(abc.ABC):
    @abc.abstractmethod
    def apply_gate(self, gate, *params, adjoint=False):
        raise NotImplementedError()

    @abc.abstractmethod
    def measure_all(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def measure(self, target):
        raise NotImplementedError()

    @abc.abstractmethod
    def yield_state(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def to_dirac(self):
        raise NotImplementedError()

    def _check_in_range(self, target):
        if target < 0 or target >= self.size:
            raise Exception(
                'Can\'t access {}[{}]: register index out of range (register size {})'.format(
                    self.name, target, self.size
                )
            )
