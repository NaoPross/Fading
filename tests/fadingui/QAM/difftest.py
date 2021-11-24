import matplotlib.pyplot as plt
import numpy as np

samp_rate = 32e3
sps = 4

data = np.fromfile("modulated_nodiff.dat", dtype=np.complex64)
samples = data[:sps*120:sps]

# plt.plot(samples.real, samples.imag, ".-")
plt.plot(samples.real, ".-")
plt.plot(samples.imag, ".-")
plt.show()
