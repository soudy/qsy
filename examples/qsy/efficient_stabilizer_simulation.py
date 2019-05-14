from qsy.backends import CHPBackend
from qsy import QuantumRegister, gates

qr = QuantumRegister(500, backend=CHPBackend)

for i in range(250):
    qr.apply_gate(gates.H, i)

for i in range(250):
    qr.apply_gate(gates.CX, 0, i + 250)

measurement = qr.measure_all()
print(measurement)
