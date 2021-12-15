#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Sara Cinzia Halter, Naoki Pross.

import os
import socket
from urllib.parse import urlparse

import numpy as np
from gnuradio import gr

from fadingui.logger import get_logger
log = get_logger("netsink")

class netsink(gr.sync_block):
    """
    Sink that sends the data over the network using UDP.
    Keep in mind that is quite slow.
    """
    def __init__(self, address, dtype, vlen):
        to_numpy = {
            "complex": np.complex64,
            "float": np.float32,
            "int": np.int32,
            "short": np.short,
            "byte": np.byte,
        }

        dt = to_numpy[dtype]
        if vlen > 1:
            dt = np.dtype(dt, (vlen,))

        gr.sync_block.__init__(self,
            name="Network Sink",
            in_sig=[dt],
            out_sig=None)

        # Create a socket and parse remote machine url
        self.url = urlparse(address)
        self.srv = None

        if self.url.scheme == "udp":
            log.debug(f"Creating UDP socket to {self.srv}")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.srv = (self.url.hostname, self.url.port)
            self.socket.connect(self.srv)

        elif self.url.scheme == "file":
            log.debug(f"Creating UNIX file socket to {self.url.path}")
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            self.srv = self.url.path
            try:
                self.socket.connect(self.srv)
            except FileNotFoundError:
                log.error("Cannot find socket file, is the server (GUI) running?")
                raise

        else:
            raise NotImplemented


    def send(self, data):
        """
        Send the data to self.srv

        @param data Data as python bytes
        @return Number of bytes that were actually sent
        """
        assert type(data) == bytes
        try:
            return self.socket.sendto(data, self.srv)
        except socket.error as err:
            log.debug(f"No data was sent: {err}")
            return 0

    def encode(self, data):
        """
        Encode the data into a dead simple format

        @param data Array like type
        @return Bytes of ASCII encoded comma separated string of numbers
        """
        # FIXME: this could be (very) slow, is there a faster way with numpy?
        # Maybe numpy.array2string
        values = "[" + ",".join(map(str, data)) + "]"
        return bytes(values, "ascii")

    def work(self, input_items, output_items):
        # send only every k-th sample
        inp = input_items[0][::2]
        inp_len = len(inp)
        blocksize = 1024

        # Check that the packet is not huge
        if len(inp) < blocksize:
            self.send(self.encode(inp))
        else:
            # compute how to split inp into blocks
            nblocks = inp_len // blocksize
            index = blocksize * nblocks

            # send blocks
            blocks = np.array(inp[:index]).reshape((blocksize, nblocks))
            for block in blocks:
                self.send(self.encode(block))

            # sent the rest
            self.send(self.encode(inp[index:]))

        return len(inp)
