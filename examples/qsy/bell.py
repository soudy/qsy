from qsy import QuantumRegister, gates

qr = QuantumRegister(2)
qr.apply_gate(gates.H, 0)
qr.apply_gate(gates.C(gates.X), 0, 1)

print(qr.to_dirac())
