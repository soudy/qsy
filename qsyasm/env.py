from qsy import QuantumRegister, ClassicalRegister

class Env:
    def __init__(self):
        self.qrs = {}
        self.crs = {}

    def qr(self, name):
        return self.qrs[name]

    def cr(self, name):
        return self.crs[name]

    def create_qr(self, name, size):
        self.qrs[name] = QuantumRegister(size)

    def create_cr(self, name, size):
        self.crs[name] = ClassicalRegister(size)
