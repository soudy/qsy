qreg[5] q
creg[4] c

h q[0]
h q[1]
h q[2]
h q[3]

x q[4]

; estimate phase of phi = 12(2π)/16
crz(2**0 * (12*2*pi)/16) q[3], q[4]
crz(2**1 * (12*2*pi)/16) q[2], q[4]
crz(2**2 * (12*2*pi)/16) q[1], q[4]
crz(2**3 * (12*2*pi)/16) q[0], q[4]

; inverse quantum fourier transform
h q[0]

adj crz(pi/2**1) q[1], q[0]
h q[1]

adj crz(pi/2**1) q[2], q[1]
adj crz(pi/2**2) q[2], q[0]
h q[2]

adj crz(pi/2**1) q[3], q[2]
adj crz(pi/2**2) q[3], q[1]
adj crz(pi/2**3) q[3], q[0]
h q[3]

; swap to get correct result from iqft
cx q[3], q[0]
cx q[0], q[3]
cx q[3], q[0]

cx q[2], q[1]
cx q[1], q[2]
cx q[2], q[1]

; measure to get phase approximation
meas q[0], c[0]
meas q[1], c[1]
meas q[2], c[2]
meas q[3], c[3]
