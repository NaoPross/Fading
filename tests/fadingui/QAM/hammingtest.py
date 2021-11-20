#!/usr/bin/env python3
import numpy as np
from fadingui import frame_obj

f = frame_obj([1,0], 10)
q = np.random.randint(0, 2, size=26)

parity = f.parity(q)
enc = np.concatenate([q, parity])

print(q)
print(parity)
print(enc)
print(f.syndrome(enc))
