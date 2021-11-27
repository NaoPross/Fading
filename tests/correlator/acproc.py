#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import acgen

# Parameters
# samples per symbol
sps = 4
# number of initial bytes (to ignore)
nzeros = 10
# length of the access code in bytes
aclen = 2

# Create samples
print("Modulating symbols")
acgen.main()

# Extract one sequence
print("Extracting symbol sequence")

# raw data
data = np.fromfile("acgen.dat", dtype=np.complex64)
plt.plot(data.real)
plt.plot(data.imag)
plt.title("Raw Data (time domain)")
plt.show()

# take only symbols
symbols = data[1::sps]
plt.plot(symbols.real, symbols.imag)
plt.title("Symbols only (constellation)")
plt.show()

# where ac symbols start, in symbols
ac_start = nzeros * 8
ac_end = ac_start + aclen * 8

ac = symbols[ac_start:ac_end]

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.tight_layout()

ax1.plot(ac.real, ac.imag)
ax1.set_title("Symbols of Access Code (constellation)")

ax2.plot(ac.real, ".-")
ax2.plot(ac.imag, ".-")
ax2.set_title("Symbols of Access Code (time)")
plt.show()

fir = list(np.conj(ac[::-1]))

# print the symbols
print(f"Generated {len(ac)} symbols from a {aclen} byte sequence")
print("Reversed symbols (for FIR filter):")
print(fir)
