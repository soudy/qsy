#! /usr/bin/env python3

from qsy import QuantumRegister, ClassicalRegister, gates

qr = QuantumRegister(10)
qr.apply_gate(gates.H, 0)
qr.apply_gate(gates.H, 1)
qr.apply_gate(gates.H, 2)
qr.apply_gate(gates.H, 9)
print(qr.to_dirac())
qr.measure(9)
print(qr.to_dirac())
