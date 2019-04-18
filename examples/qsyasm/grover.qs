qreg[3] q
creg[2] c

; prep
h q[0]
h q[1]

x q[2]
h q[2]

; oracle
ccx q[0], q[1], q[2]

; post-process
h q[0]
h q[1]

x q[0]
x q[1]

cz q[0], q[1]

x q[0]
x q[1]

h q[0]
h q[1]

meas q[0], c[0]
meas q[1], c[1]
