# qsy
A quantum computer state vector simulator in Python.

## Example
The following code creates an entangled state and prints its state vector in
Dirac notation.
```python
from qsy import QuantumRegister, gates

qr = QuantumRegister(2)
qr.apply_gate(gates.H, 0)
qr.apply_gate(gates.C(gates.X), 0, 1)
print(qr.to_dirac())
```
The output will be:
```
+0.7071|00> +0.7071|11>
```
