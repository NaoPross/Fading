#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Sara Cinzia Halter, Naoki Pross.

import socket
from urllib.parse import urlparse

import numpy as np
from gnuradio import gr

class netsink(gr.sync_block):
    """
    Sink that sends the data over the network using UDP.
    Keep in mind that is quite slow.
    """
    def __init__(self, address, dtype, vlen):
        dt = np.dtype(dtype, (vlen,)) if vlen > 1 else dtype
        print(dt)

        gr.sync_block.__init__(self,
            name="Network Sink",
            in_sig=[dt],
            out_sig=None)

        # Create a socket and parse remote machine url
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.url = urlparse(address)
        self.srv = (self.url.hostname, self.url.port)

    def send(self, data):
        """
        Send the data to self.srv

        @param data Data as python bytes
        @return Number of bytes that were actually sent
        """
        assert type(data) == bytes
        return self.socket.sendto(data, self.srv)

    def encode(self, data):
        """
        Encode the data into a dead simple format

        @param data Array like type
        @return Bytes of ASCII encoded comma separated string of numbers
        """
        # FIXME: this could be (very) slow, is there a faster way with numpy?
        values = "[" + ",".join(map(str, data)) + "]"
        return bytes(values, "ascii")

    def work(self, input_items, output_items):
        # FIXME: it is probably better NOT to send *every* sample
        inp = input_items[0]
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
