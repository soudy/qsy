qreg[7] q

; uncomment to encode |1>, otherwise encode |0>
; x q[0]

cx q[0], q[1]
cx q[0], q[2]

h q[4]
h q[5]
h q[6]

cx q[4], q[3]
cx q[4], q[2]
cx q[4], q[1]

cx q[5], q[3]
cx q[5], q[2]
cx q[5], q[0]

cx q[6], q[3]
cx q[6], q[1]
cx q[6], q[0]

