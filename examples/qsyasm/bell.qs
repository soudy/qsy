qreg[2] q
creg[2] c

h q[0]
c(x) q[0], q[1]

meas q, c
meas q[0], c[0]
; or:
; meas q[0], c[0]
; meas q[1], c[1]
