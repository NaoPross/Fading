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
        gr.sync_block.__init__(self,
            name="Network Sink",
            in_sig=[],
            out_sig=None)

        # Create a socket and parse remote machine url
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.url = urlparse(sock_addr)
        self.srv = (self.srv.hostname, self.srv.port)

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
        # no data (what are you doing?)
        if not data:
            return bytes()

        values = "[" + ",".join(map(str, data)) + "]"
        return bytes(values, "ascii")

    def work(self, input_items, output_items):
        inp = input_items[0]

        # TODO: Check that inp has a reasonable size
        self.send(self.encode(inp))

        return len(input_items[0])

