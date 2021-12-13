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
    def __init__(self, url, dtype, timeout=0.05):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.url = urlparse(url)
        self.dtype = dtype
        self.timeout = timeout

    def __del__(self):
        self.sock.close()

    def bind(self):
        self.sock.setblocking(False)
        self.sock.bind((self.url.hostname, self.url.port))
        # self.sock.listen()

    def read(self, nblocks):
        # TODO: run in a separate thread (it will be painful to implement)
        ready, _w, _x = select.select([self.sock], [], [], self.timeout)
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
                try:
                    return list(map(self.dtype, samples))
                except ValueError:
                    return []

        # convert each chunk into a list of samples
        chunk_values = map(chunk_to_samples, chunks)

        # flatten list of lists into a single list
        values = sum(chunk_values, [])

        return values

class network_plot(udpsource):
    """
    Wraps a udpsource while at the same time intefacing with DearPyGUI as a plot element.
    """
    def __init__(self, url, dtype, nsamples , **kwargs):
        udpsource.__init__(self, url, dtype)
        self.nsamples = nsamples

        self._init_buffers()
        self._init_dpg_plot(**kwargs)

        # listen for connections
        self.bind()

    def _init_buffers(self):
        # create buffers for x and y values
        self.xvalues = RingBuffer(capacity=self.nsamples, dtype=np.dtype(self.dtype))
        self.yvalues = RingBuffer(capacity=self.nsamples, dtype=np.dtype(self.dtype))

        self.xvalues.extend(np.arange(0, self.nsamples))
        self.yvalues.extend(np.zeros(self.nsamples))

    def _init_dpg_plot(self, **kwargs):
        self.plot = dpg.plot(**kwargs)

    # Map `with' expressions to the underlying plot
    def __enter__(self):
        return self.plot.__enter__()

    def __exit__(self, t, val, tb):
        self.plot.__exit__(t, val, tb)

    @property
    def xdata(self):
        # unwrap ringbuffer
        return np.array(self.xvalues)

    @property
    def ydata(self):
        # unwrap ringbuffer
        return np.array(self.yvalues)

    def refresh_series(self, tag):
        new_values = self.read(10)

        if new_values:
            self.yvalues.extendleft(new_values)
            dpg.set_value(tag, [self.xdata, self.ydata])


class network_constellation_plot(network_plot):
    """
    Special case of a plot, where complex numbers are drawn into a scatter plot
    """
    def __init__(self, url, nsamples, **kwargs):
        network_plot.__init__(self, url, np.complex64, nsamples)

    def _init_buffers(self):
        self.xvalues = RingBuffer(capacity=self.nsamples, dtype=np.float32)
        self.yvalues = RingBuffer(capacity=self.nsamples, dtype=np.float32)

        self.xvalues.extend(np.zeros(self.nsamples))
        self.yvalues.extend(np.zeros(self.nsamples))

    def refresh_series(self, tag):
        new_values = self.read(1)

        if new_values:
            self.xvalues.extendleft(np.real(new_values))
            self.yvalues.extendleft(np.imag(new_values))

            dpg.set_value(tag, [self.xdata, self.ydata])
