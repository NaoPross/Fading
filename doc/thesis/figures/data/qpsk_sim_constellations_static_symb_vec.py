#!/usr/bin/env python3

import os
import numpy as np

DATA_DIR = "./figures/data/flowgraphs"
SPS = 4

channel   = np.fromfile(f"{DATA_DIR}/qpsk_channel_static_symb_vec.dat", dtype=np.complex64)[::SPS]
sync      = np.fromfile(f"{DATA_DIR}/qpsk_sync_static_symb_vec.dat", dtype=np.complex64)
equalized = np.fromfile(f"{DATA_DIR}/qpsk_equalized_static_symb_vec.dat", dtype=np.complex64)
locked    = np.fromfile(f"{DATA_DIR}/qpsk_locked_static_symb_vec.dat", dtype=np.complex64)

samples = [channel, sync, equalized, locked]

# print(list(map(len, samples)))

start = 1e3
end = start +800

get_range = lambda arr: arr[int(start):int(end):2]
get_parts = lambda v: (np.real(v), np.imag(v))

values = map(get_range, samples)
parts = [p for v in map(get_parts, values) for p in v]
data = np.array(list(zip(*parts)))

# save to file
location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
name, _ = os.path.splitext(os.path.basename(__file__))
filename = os.path.join(location, name + ".dat")
np.savetxt(filename, data, fmt='%.6e')
