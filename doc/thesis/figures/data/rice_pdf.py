#!/usr/bin/env python3

import os
import numpy as np

a = np.linspace(0, 3, num=100)

ps = []
for k in [0, 2, 5, 10]:
    p = 2 * a * (1 + k) * np.exp(-k - (a**2) * (k + 1)) \
            * np.i0(2 * a * np.sqrt(k * (1 + k)))

    ps += [p]


data = np.array(list(zip(a, *ps)))

# save to file
location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
name, _ = os.path.splitext(os.path.basename(__file__))
filename = os.path.join(location, name + ".dat")
np.savetxt(filename, data, fmt='%.6e')
