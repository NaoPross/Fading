import os
import numpy as np

def load_samples(fname, dtype=np.complex64):
    set_name, _ = os.path.splitext(os.path.basename(fname))

    data_dir = "./figures/data/flowgraphs"
    sps = 4

    channel      = np.fromfile(f"{data_dir}/channel_{set_name}.dat", dtype=dtype)[::sps]
    synchronized = np.fromfile(f"{data_dir}/synchronized_{set_name}.dat", dtype=dtype)
    equalized    = np.fromfile(f"{data_dir}/equalized_{set_name}.dat", dtype=dtype)
    locked       = np.fromfile(f"{data_dir}/locked_{set_name}.dat", dtype=dtype)

    return channel, synchronized, equalized, locked

def save_to_file(fname, data, headers):
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(fname)))
    name, _ = os.path.splitext(os.path.basename(fname))
    filename = os.path.join(location, name + ".dat")
    np.savetxt(filename, data, fmt='%.6e\t', header="\t".join(headers), comments='')

