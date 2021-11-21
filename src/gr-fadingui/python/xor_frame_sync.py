#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Naoki Pross.


import numpy as np
from numpy_ringbuffer import RingBuffer

from gnuradio import gr

from fadingui.logger import get_logger
log = get_logger("xor_frame_sync")


class xor_frame_sync(gr.sync_block):
    """
    Performs a frame synchronization by XOR matching a preamble bit sequence
    """
    def __init__(self, sync_pattern, buffer_size):
        # TODO: buffer size should be in packets
        gr.sync_block.__init__(self,
            name="xor_frame_sync",
            in_sig=[np.byte],
            out_sig=[np.byte])

        # binary pattern to match
        self.pattern = np.unpackbits(np.array(sync_pattern, dtype=np.uint8))[::-1]
        self.nbytes = len(sync_pattern)
        self.nbits = len(self.pattern)

        log.debug(f"Loaded pattern {self.pattern} length={self.nbits}")
        assert(self.nbits % 8 == 0)

        # packed buffer to delay the data
        self.delaybuf = RingBuffer(buffer_size, dtype=np.uint8)
        self.delay = 0

        # unpacked buffer to compute correlation values, initially filled with zeros
        self.corrbuf = RingBuffer(self.nbits)
        self.corrbuf.extend(np.zeros(self.nbits))

        # buffer to store correlation values
        self.xcorrs = RingBuffer(buffer_size)

        # synchronization state
        self.synchronized = False

    def xcorrelation(self, v):
        """
        Compute the binary correlations between the stored pattern and
        correlation buffer, while shifting v into the buffer.

        Binary correlation between two bit vectors is just size of the
        vector(s) minus the number of bits that differ.
        """
        v_arr = np.array(v, dtype=np.uint8)
        for b in np.unpackbits(v_arr):
            self.corrbuf.appendleft(b)
            yield self.nbits - np.sum(np.logical_xor(self.corrbuf, self.pattern))

    def work(self, input_items, output_items):
        """
        Process the inputs, that means:

            - Check that the buffer is synchronized, i.e. there is the sync
              pattern appears every k bits, where k is the size of the packet.

            - If the buffer is not synchronized, compute a binary cross
              correlation to find how much the stream should be delayed.

        Notes:

            - Even though the block input is of type np.byte, inp is an array
              of 255 bytes, probably for performance reasons.
              TODO: block processing
        """
        inp = input_items[0]
        out = output_items[0]

        if not self.synchronized:
            for v in inp:
                # compute the cross correlation
                xcs = self.xcorrelation(v)

                # add cross correlations to buffer and save value
                self.xcorrs.extend(list(xcs))
                self.delaybuf.appendleft(v)

            peak = np.argmax(self.xcorrs)
            if self.xcorrs[peak] == self.nbits:
                self.delay = peak
                self.synchronized = True
                log.debug(f"Synchronized with delay={peak}")

            else:
                self.synchronized = False
                log.warning(f"Did not find a peak (max={self.xcorrs[peak]}, should be {self.nbits})")


        # return data with delay
        out[:] = self.delaybuf[self.delay]

        return len(output_items[0])

