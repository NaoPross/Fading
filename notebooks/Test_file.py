# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 16:05:59 2021

@author: sarah
"""

import numpy as np
import matplotlib.pyplot as plt

delay = 5.33
ampl = 1
print(f"Tap with amplitude={ampl}, delay={delay}")

order = 2 * np.floor(delay) + 1 #N
print(f"Creating filter of order N={order}")

samples = np.arange(0, order +1) 

h = ampl*(np.sinc(samples-delay)) #sinc

# plt.stem(samples, h)
# plt.show()

t = np.arange(50)

signal = np.sin(2 * np.pi * t * 0.05)

signal_shifted = np.convolve(h, signal, mode='full')

#Time PLot
plt.xlabel('Delay')
plt.ylabel('Amplitude')
#plt.title('')
plt.plot(t, signal)
plt.grid(True)
plt.show()
plt.plot(signal_shifted)