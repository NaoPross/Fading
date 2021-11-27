import select
import socket
from urllib.parse import urlparse

import numpy as np
from numpy_ringbuffer import RingBuffer
import dearpygui.dearpygui as dpg


class udpsource:
    """
    Creates an UDP listening socket
    """
    def __init__(self, url):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.url = urlparse(url)

    def __del__(self):
        self.sock.close()

    def bind(self):
        self.sock.setblocking(False)
        self.sock.bind((self.url.hostname, self.url.port))
        # self.sock.listen()

    def read(self, nbytes):
        ready_to_read, ready_to_write, in_err = \
                select.select([self.sock], [], [], 1)

        if ready_to_read:
            data = sock.recv(nbytes)
            print(data)
        else:
            return None


class network_plot(udpsource):
    def __init__(self, url, nsamples, **kwargs):
        udpsource.__init__(self, url)

        self.nsamples = nsamples
        self.plot = dpg.plot(**kwargs)

        # create buffer and fill with zeroes
        self.buffer = RingBuffer(capacity=nsamples, dtype=(float, 2))
        for i in range(nsamples):
            # TODO: remove random data used for testing
            self.buffer.append(np.array([i, 1 + np.random.rand() / 5]))

        self.bind()

    def __enter__(self):
        return self.plot.__enter__()

    def __exit__(self, t, val, tb):
        self.plot.__exit__(t, val, tb)

    @property
    def x_data(self):
        return np.array(self.buffer[:,0])

    @property
    def y_data(self):
        return np.array(self.buffer[:,1])

    def refresh_series(self, tag):
        dpg.set_value(tag, [self.x_data, self.y_data])
        pass
