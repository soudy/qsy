qreg q[5]
creg c[2]

h q[0]
h q[1]
h q[2]

z q[0]

h q[3]
h q[4]

cx q[3], q[0]
cx q[3], q[1]

cx q[4], q[1]
cx q[4], q[2]

h q[3]
h q[4]

meas q[3], c[0]
meas q[4], c[1]
