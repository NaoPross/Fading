import select
import socket
from urllib.parse import urlparse
import re

import numpy as np
from numpy_ringbuffer import RingBuffer
import dearpygui.dearpygui as dpg


class udpsource:
    """
    Creates an UDP listening socket
    """
    def __init__(self, url, dtype):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.url = urlparse(url)
        self.dtype = dtype

    def __del__(self):
        self.sock.close()

    def bind(self):
        self.sock.setblocking(False)
        self.sock.bind((self.url.hostname, self.url.port))
        # self.sock.listen()

    def read(self, nblocks):
        ready, _, _ = select.select([self.sock], [], [])
        if not ready:
            return None

        # read from socket
        blocksize = 1024 * 4
        string = ready[0].recv(nblocks * blocksize).decode("ascii")

        # decode string, remove empty values
        chunks = filter(None, re.split(r"\[(.+?)\]", string))

        def chunk_to_samples(chunk):
            samples = chunk.split(",")
            if samples:
                return list(map(self.dtype, samples))

        # convert each chunk into a list of samples
        chunk_values = map(chunk_to_samples, chunks)

        # flatten list of lists into a single list
        values = sum(chunk_values, [])

        return values

class network_plot(udpsource):
    def __init__(self, url, dtype, nsamples, **kwargs):
        udpsource.__init__(self, url, dtype)

        # create buffers for x and y values
        self.nsamples = nsamples
        self.xvalues = np.arange(0, self.nsamples)
        self.yvalues = RingBuffer(capacity=self.nsamples, dtype=np.dtype(dtype))
        self.yvalues.extend(np.zeros(self.nsamples))

        # create a plot
        self.plot = dpg.plot(**kwargs)
        self.bind()

    # Map `with' expressions to the underlying plot
    def __enter__(self):
        return self.plot.__enter__()

    def __exit__(self, t, val, tb):
        self.plot.__exit__(t, val, tb)

    @property
    def xdata(self):
        return self.xvalues

    @property
    def ydata(self):
        return np.array(self.yvalues)

    def refresh_series(self, tag):
        new_values = self.read(1)

        if new_values:
            self.yvalues.extendleft(new_values)
            dpg.set_value(tag, [self.xdata, self.ydata])
