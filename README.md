# qsy
A quantum computer state vector simulator and quantum assembly language in
Python.

## qsy
qsy is a Python library for simulating quantum circuits.

### Example
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

## qsyASM
qsyASM is a quantum assembly language acting as front-end for qsy. It allows
you to quickly write and debug quantum programs.

### Example
The following qsyASM program creates an entangled state and measures to a
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
q[2]: +1.0000|11>
      0.0 | 00
      0.0 | 01
      0.0 | 10
      1.0 | 11
c[2]: 11
```
More examples such as the Quantum Phase Estimation algorithm can be found in the
[examples/qsyasm](examples/qsyasm) folder.

### Syntax
The structure of a qsyASM program consists of a list of instructions. An
instruction is defined as an operation followed by its arguments.

#### Operations
The instruction
```asm
cx q[0], q[1]
```
applies a CNOT operation with control qubit `q[0]` and target qubit `q[1]`.
Some operations take an angle (in radian) as argument. The parameterized operation
```asm
rz(pi/2) q[0]
```
rotates `q[0]` π/2 radians around the Z axis. Expressions are allowed in
parameterized operations. Expression operators supported are `+`, `-`, `*`, `/`
and `**` (power). The variable `pi` is available for convenience.

##### List of operations
| Gate     |  qsyASM operation                |
|----------|----------------------------------|
| Pauli I  | `i target`                       |
| Pauli X  | `x target`                       |
| Pauli Y  | `y target`                       |
| Pauli Z  | `z target`                       |
| Hadamard | `h target`                       |
| S        | `s target`                       |
| Sdag     | `sdag target`                    |
| T        | `t target`                       |
| Tdag     | `tdag target`                    |
| Rx       | `rx(angle) target`               |
| Ry       | `ry(angle) target`               |
| Rz       | `rz(angle) target`               |
| CNOT     | `cx control, target`             |
| CZ       | `cz control, target`             |
| CRx      | `crx(angle) control, target`     |
| CRy      | `cry(angle) control, target`     |
| CRz      | `crz(angle) control, target`     |
| Toffoli  | `ccx controlA, controlB, target` |

#### Registers
Defining a quantum register is done with the `qreg` operation. The instruction
```asm
qreg[5] q
```
defines a 5 qubit quantum register named `q`. Likewise, a classical register (useful for measuring) can be defined as
```asm
creg[5] c
```
Qubits in a quantum register are initiated to |0⟩, and bits in a classical register to 0.

#### Measurement
Measurement can be done on individual qubits, or a complete quantum state. The program
```asm
qreg[5] q
creg[1] c

h q[0]

meas q[0], c[0]
```
measures `q[0]` to `c[0]`, collapsing the state and storing the result in `c[0]`. The measurement result can be ignored by only passing one argument to `meas`:
```asm
meas q[0]
```

To measure a complete quantum state you can pass the whole quantum and classical register:
```asm
qreg[3] q
creg[3] c

; 3 qubit GHZ state
h q[0]
cx q[0], q[1]
cx q[0], q[2]

meas q, c
```
collapsing the quantum register `q` and storing the measurement result in `c`. This only works when the quantum register and classical register are equal in size.
