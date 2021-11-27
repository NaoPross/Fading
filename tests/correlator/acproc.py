#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from acgen import acgen

# parameters
access_code_bits = [ 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, ]
access_code = list(np.packbits([0] * 3 + access_code_bits))
padding_zeros = 10

# Create samples
print(f"Modulating symbols for access code {access_code_bits} = {access_code} with after {padding_zeros} empty bytes")
gen = acgen()
gen.set_access_code(access_code)
gen.set_padding_zeros(padding_zeros)

gen.start()
gen.wait()

# Extract one sequence
print("Extracting symbol sequence")

# raw data
data = np.fromfile("acgen.dat", dtype=np.complex64)
plt.plot(data.real)
plt.plot(data.imag)
plt.title("Raw Data (time domain)")
plt.show()

# take only symbols
symbols = data[1::gen.sps]

plt.plot(symbols.real, symbols.imag)
plt.title("Symbols only (constellation)")
plt.show()

# where ac symbols start, in symbols
ac_start = (padding_zeros) * 8 + 3 # plus three because code is 13 bits
ac_end = ac_start + int(np.ceil(len(access_code_bits) / 2.)) # divided by two because QPSK

ac = symbols[ac_start:ac_end]

print(f"Generated {len(ac)} (left padded) symbols from a {len(access_code_bits)} bit sequence")
print(list(ac))

print(f"Upsampled to {gen.sps} samples per symbos")
print(sum([[i, i, i, i] for i in ac], []))

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.tight_layout()

ax1.plot(ac.real, ac.imag)
ax1.set_title("Symbols of Access Code (constellation)")

ax2.plot(ac.real, ".-")
ax2.plot(ac.imag, ".-")
ax2.set_title("Symbols of Access Code (time)")
plt.show()

fir = list(np.conj(ac[::-1]))

# Print the symbols
print("Reversed complex conjugate symbols (for FIR filter):")
print(fir)

# Compute cross correlation

xc = np.convolve(fir, ac)

plt.plot(np.abs(xc))
plt.title("Cross correlation (FIR)")
plt.show()
