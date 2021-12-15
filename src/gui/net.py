import os
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
    def __init__(self, url, dtype, timeout=0.05, blocksize=1024):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.url = urlparse(url)
        self.dtype = dtype
        self.timeout = timeout
        self.blocksize = blocksize

        if self.url.scheme == "udp":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif self.url.scheme == "file":
            try:
                os.unlink(self.url.path)
            except OSError:
                if os.path.exists(self.url.path):
                    raise

            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        else:
            raise NotImplemented

    def __del__(self):
        self.sock.close()

    def bind(self):
        self.sock.setblocking(False)
        if self.url.scheme == "udp":
            self.sock.bind((self.url.hostname, self.url.port))
        elif self.url.scheme == "file":
            self.sock.bind(self.url.path)

        # self.sock.listen(1)

    def read(self, nblocks):
        # TODO: run in a separate thread (it will be painful to implement)
        ready, _w, _x = select.select([self.sock], [], [], self.timeout)
        if not ready:
            return None

        # read from socket
        string = ready[0].recv(nblocks * self.blocksize).decode("ascii")

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

class network_value(udpsource):
    def __init__(self, url, dtype, refresh_func):
        udpsource.__init__(self, url, dtype, blocksize=16)

        self._refresh = refresh_func
        self.value = None

        self.bind()

    def read(self):
        return udpsource.read(self, 3)

    def refresh(self):
        self.value = self.read()
        if self.value:
            self._refresh(self.value)


class network_plot(udpsource):
    """
    Wraps a udpsource while at the same time intefacing with DearPyGUI as a plot element.
    """
    def __init__(self, url, dtype, nsamples, **kwargs):
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
        if "tag" in kwargs:
            self.tag = kwargs["tag"]

            self.series_tag = f"{self.tag}_series"
            self.xaxis_tag = f"{self.tag}_xaxis"
            self.yaxis_tag = f"{self.tag}_yaxis"
            self.window_tag = f"window_{self.tag}"

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
        network_plot.__init__(self, url, np.complex64, nsamples, **kwargs)

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
