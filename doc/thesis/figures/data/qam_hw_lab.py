#!/usr/bin/env python3

import utils
import numpy as np

# get array of samples [channel, synchronized, equalized, locked]
samples = utils.load_samples(__file__)

# range of samples we want to show
start = 20e3
end = start +400

# select every second samples
select_samples = lambda arr: arr[int(start):int(end):6]
values = map(select_samples, samples)

# split into imaginary and real parts
get_parts = lambda v: (np.real(v), np.imag(v))
parts = [p for v in map(get_parts, values) for p in v]

# zip data and add header
data = np.array(list(zip(*parts)))
headers = [
    "channel_re",      "channel_im",
    "synchronized_re", "synchronized_im",
    "equalized_re",    "equalized_im",
    "locked_re",       "locked_im"
]

# save to file
utils.save_to_file(__file__, data, headers)
