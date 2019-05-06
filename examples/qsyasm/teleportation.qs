qreg[3] q

; prepare state to be teleported: |+i>
h q[0]
s q[0]

; create EPR pair
h q[1]
cx q[1], q[2]

cx q[0], q[1]
h q[0]

meas q[0]
cz q[0], q[2]

meas q[1]
cx q[1], q[2]
