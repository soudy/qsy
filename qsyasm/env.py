from .error import QsyASMError
from qsy import QuantumRegister, ClassicalRegister


class Env:
    def __init__(self):
        self.qrs = {}
        self.crs = {}

    def qr(self, name):
        if name not in self.qrs:
            raise IndexError('Undefined quantum register "{}"'.format(name))

        return self.qrs[name]

    def cr(self, name):
        if name not in self.crs:
            raise IndexError('Undefined classical register "{}"'.format(name))

        return self.crs[name]

    def create_qr(self, name, size, backend):
        self.qrs[name] = QuantumRegister(size, name, backend=backend)

    def create_cr(self, name, size):
        self.crs[name] = ClassicalRegister(size, name)
