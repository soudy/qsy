from qsy import ClassicalRegister, QuantumRegister
from qsy.error import RegisterIndexError

from .error import QsyASMError


class Env:
    def __init__(self):
        self.qrs = {}
        self.crs = {}

    def qr(self, name):
        if name not in self.qrs:
            raise RegisterIndexError('Undefined quantum register "{}"'.format(name))

        return self.qrs[name]

    def cr(self, name):
        if name not in self.crs:
            raise RegisterIndexError('Undefined classical register "{}"'.format(name))

        return self.crs[name]

    def create_qr(self, name, size, backend):
        self.qrs[name] = QuantumRegister(size, name, backend=backend)

    def create_cr(self, name, size):
        self.crs[name] = ClassicalRegister(size, name)
