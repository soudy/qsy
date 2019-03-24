# qsy
A quantum computer state vector simulator in Python.

## Example
The following code creates an entangled state and prints its state vector in
Dirac notation.
```python
from qsy import QuantumRegister, gates

qr = QuantumRegister(2)
qr.apply_gate(gates.H, 0)
qr.apply_gate(gates.CX, 0, 1)

print(qr.to_dirac())
```
The output will be:
```
+0.7071|00> +0.7071|11>
```

### qsyASM
Equivalently, the following qsyASM program does the same, and measures to a
classical register:
```asm
qreg[2] q
creg[2] c

h q[0]
cx q[0], q[1]

meas q, c
```
Running it:
```bash
$ qsyasm examples/qsyasm/bell.qs
q[2]: [0. 0. 0. 1.] (+1.0000|11>)
      0.0 | 00
      0.0 | 01
      0.0 | 10
      1.0 | 11
c[2]: 11
```
