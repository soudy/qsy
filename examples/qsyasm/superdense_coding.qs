qreg[2] q
creg[2] c

h q[0]
cx q[0], q[1]

; encode 11
x q[1]
z q[1]

; encode 01
; x q[1]

; encode 10
; z q[1]

cx q[0], q[1]
h q[0]

meas q, c
