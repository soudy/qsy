from .error import QsyASMError
from qsy import QuantumRegister, ClassicalRegister

class Env:
    def __init__(self):
        self.qrs = {}
        self.crs = {}

    def qr(self, name):
        if not name in self.qrs:
            raise QsyASMError('Undefined quantum register "{}"'.format(name))

        return self.qrs[name]

    def cr(self, name):
        if not name in self.crs:
            raise QsyASMError('Undefined classical register "{}"'.format(name))

        return self.crs[name]

    def create_qr(self, name, size):
        self.qrs[name] = QuantumRegister(size, name)

    def create_cr(self, name, size):
        self.crs[name] = ClassicalRegister(size, name)
