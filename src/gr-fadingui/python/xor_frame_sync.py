#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Naoki Pross.


import numpy as np
from numpy_ringbuffer import RingBuffer

from gnuradio import gr


class xor_frame_sync(gr.sync_block):
    """
    docstring for block xor_frame_sync
    """
    def __init__(self, sync_pattern, buffer_size):
        gr.sync_block.__init__(self,
            name="xor_frame_sync",
            in_sig=[np.byte],
            out_sig=[np.byte])

        # binary pattern to match
        self.pattern = np.array(sync_pattern, dtype=np.dtype("uint8"))
        self.nbits = len(sync_pattern)

        # buffer to delay the data
        self.delay_fifo = RingBuffer(buffer_size, dtype=np.byte)

        # buffers to store cross correlation data
        self.xcorr = RingBuffer(buffer_size, dtype=np.dtype("uint8"))

        # synchronization state
        self.synchronized = False
        self.delay = 0

    def xcorrelation(self):
        """
        Compute the binary correlation between the stream and the stored
        pattern. Binary correlation between two bit vectors is just size of the
        vector(s) minus the number of bits that differ.
        """
        unpacked = np.unpackbits(self.delay_fifo[0])
        return self.nbits - sum(np.logical_xor(unpacked, self.pattern))

    def work(self, input_items, output_items):
        """
        Process the inputs, that means:

            - Check that the buffer is synchronized, i.e. there is the sync
              pattern appears every k bits, where k is the size of the packet.

            - If the buffer is not synchronized, compute a binary cross
              correlation to find how by much the stream should be delayed.
        """
        inp = input_items[0]
        out = output_items[0]

        # Add data to delay buffer
        self.delay_fifo.appendleft(inp)

        # TODO: check for synchronization, else compute

        # Compute correlation
        if not self.synchronized:
            self.xcorr.append(self.xcorrelation())

            peak = np.argmax(self.xcorr)
            if self.xcorr[peak] != self.nbits:
                print(f"Warning! XOR correlation is not perfect (peak value = {self.xcorr[peak]})")

            self.delay = peak
            self.synchronized = True

        # return data with delay
        out[:] = self.delay_fifo[self.delay]

        return len(output_items[0])

