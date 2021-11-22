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
        self.pattern = sync_pattern
        self.nbytes = len(self.pattern)

        self.pattern_bits = np.unpackbits(np.array(self.pattern, dtype=np.uint8))[::-1]
        self.nbits = len(self.pattern_bits)

        log.debug(f"Loaded pattern {self.pattern_bits} length={self.nbits}")
        assert(self.nbits % 8 == 0)

        # packed buffer to delay the data
        self.delaybuf = RingBuffer(buffer_size, dtype=np.uint8)
        self.delay = 0

        log.debug(f"Created delay ring buffer of size {self.delaybuf.maxlen}")

        # unpacked buffer to compute correlation values, initially filled with zeros
        self.corrbuf = RingBuffer(self.nbits, dtype=np.uint8)
        self.corrbuf.extend(np.zeros(self.corrbuf.maxlen))

        # synchronization state
        self.synchronized = False

    def xcorrelation(self, v):
        """
        Compute the binary correlations between the stored pattern and
        correlation buffer, while shifting v into the buffer.

        Binary correlation between two bit vectors is just size of the
        vector(s) minus the number of bits that differ.

        @return: Number of bits of v that were shifted into the buffer
                 when the correlation matched. If no match is found
                 the return value is None.
        """
        # this could be much faster with shifts, bitwise or and xor
        # but this should do alright for the moment
        v_bits = np.unpackbits(np.array(v, dtype=np.uint8))
        for bitnr, b in enumerate(v_bits):
            self.corrbuf.appendleft(b)
            if (np.bitwise_xor(self.corrbuf, self.pattern_bits) == 0).all():
                return bitnr

        # no cross correlation found
        return None

    def work(self, input_items, output_items):
        """
        Process the inputs, that means:

            - Check that the buffer is synchronized, i.e. there is the sync
              pattern appears every k bits, where k is the size of the packet.

            - If the buffer is not synchronized, compute a binary cross
              correlation to find how much the stream should be delayed.
        """
        inp = input_items[0]
        out = output_items[0]

        inp_len = len(inp)

        if not self.synchronized:
            if inp_len > self.delaybuf.maxlen:
                log.error("Input is bigger than delay buffer")

                # FIXME: Makes the QA hang for some reason
                # raise NotImplemented

            for bytenr, value in enumerate(inp):
                # save value in the buffer
                self.delaybuf.appendleft(value)

                # compute the cross correlation
                bitnr = self.xcorrelation(value)
                if bitnr is not None:
                    # correlation was found
                    delay_bits = 8 * bytenr + bitnr

                    # FIXME: add bit delay
                    self.delay = bytenr
                    self.synchronized = True
                    log.debug(f"Synchronized with delay={self.delay} delay_bits={delay_bits}")

                    # Not aligned to bytes
                    if bitnr != 7:
                        log.error("Not implemented: byte unaligned delay")
                        self.synchronized = False
                        self.delay = 0

                        # FIXME: Makes the QA hang for some reason
                        # raise NotImplemented

                    # bigger than buffer
                    if bytenr > self.delaybuf.maxlen:
                        log.error("Too too long to synchronize, ran out of buffer memory")
                        self.synchronized = False
                        self.delay = 0

                        # FIXME: Makes the QA hang for some reason
                        # raise NotImplemented

                    # stop processing inputs
                    break

            if not self.synchronized:
                log.warning(f"Processed {inp_len} samples but could not synchronize")
        else:
            self.delaybuf.extendleft(inp)

        # return data with delay
        out[:] = self.delaybuf[self.delay]

        return len(output_items[0])

