; run this using the CHP back-end

qreg[750] q
creg[750] c

h q[50]
h q[75]
h q[100]

cx q[50], q[51]
cx q[50], q[52]
cx q[50], q[53]
cx q[50], q[54]
cx q[50], q[55]
cx q[50], q[56]
cx q[50], q[57]
cx q[50], q[58]
cx q[50], q[59]
cx q[50], q[60]

meas q, c
