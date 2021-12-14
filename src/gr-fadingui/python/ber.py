#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Sara Cinzia Halter.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import socket
from urllib.parse import urlparse

import numpy as np
from numpy_ringbuffer import RingBuffer
from gnuradio import gr

from fadingui.logger import get_logger
log = get_logger("ber")

np.set_printoptions(formatter={'int': hex})

class ber(gr.sync_block):
    """
    docstring for block ber
    """
    def __init__(self, vgl, vlen, address):
        gr.sync_block.__init__(self,
            name="ber",
            in_sig=[np.dtype(str(vlen) + "b")],
            out_sig=None)
        self.vgl=vgl
        self.vlen=vlen

        self.ber_samples = RingBuffer(capacity=2000, dtype=int)
        self.ber_samples.extend(np.zeros(self.ber_samples.maxlen))

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
        """
        # FIXME: this could be (very) slow, is there a faster way with numpy?
        # Maybe numpy.array2string
        return bytes(str(data) + "\n", "ascii")

    def ber_stats(self):
        ber_max = np.max(self.ber_samples)
        ber_min = np.min(self.ber_samples)
        ber_avg = np.sum(self.ber_samples) / self.ber_samples.maxlen

        return ber_max, ber_min, ber_avg    


    def work(self, input_items, output_items):
        inp = input_items[0]

        log.debug(f"Length: {len(inp)}")
        # log.debug(f"Inp_vector:{inp}")

        

        for i in inp:
            i = np.array(i, dtype=np.uint8)
            v = np.array(self.vgl, dtype=np.uint8) ^ i
            ber = sum(np.unpackbits(v))

            trueber = ber - 32
            if trueber < 0:
                trueber = 0
            # log.debug(f"BER {trueber} in Paket {i}")

            self.ber_samples.appendleft(trueber)


        ber_max, ber_min, ber_avg = self.ber_stats()
        log.debug(f"Statistics: {ber_max}, {ber_min}, {ber_avg}")

        #self.send(self.encode(ber_max, ber_min, ber_avg))
        self.send(self.encode(trueber))
        self.send(self.encode(ber_max))
        self.send(self.encode(ber_min))
        self.send(self.encode(ber_avg))

        return len(inp)
        #return len(input_items[0])

