import select
import socket
from urllib.parse import urlparse

import numpy as np


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

