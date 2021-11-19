#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Naoki Pross.

from functools import reduce
import operator as op

import numpy as np
from gnuradio import gr


class frame_obj(gr.basic_block):
    """
    Frame Object: Contains informations about a data frame.

      -------------------------------------------------------------------------------
      | Preamble | Padding | ID     | Data Length | Parity | Payload | Padding      |
      | k bytes  | 1 bit   | 4 bits | 22 bits     | 5 bits |         | if necessary |
      -------------------------------------------------------------------------------
                           | (31, 26) Hamming code EC      |
                           -----------------------------------

    - The preamble is user defined.
    - The ID (11 bits) + Data length (22 bits) together are a 31 bits, followed
      by 26 parity bits computed using a (31,26) hamming code.

      This constraints the maximum payload size to 64 MB and the number IDs to
      1024 (i.e. max file size is 1 GB, more than enough for many thing)

    """
    def __init__(self, preamble, payload_len):
        gr.basic_block.__init__(self, name="frame_obj",
                in_sig=None, out_sig=None)

        self.preamble = np.array(preamble, dtype=np.uint8)

        self.preamble_len = len(self.preamble)
        self.payload_len = payload_len

    @property
    def length(self):
        """Frame lenght in bytes"""
        return self.preamble_len + self.payload_len + 8

    def parity(self, bits):
        """Compute the 5 parity bits for an unpacked array of 26 bits"""
        assert(len(bits) == 26)
        # FIXME: does not work
        # gen = np.array(
        #     [[1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        #      [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        #      [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
        #      [0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
        #      [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1]],
        #     dtype=np.uint8)
        # return np.matmul(bits, gen) % 2
        return np.array([0, 0, 0, 0, 0])

    def make(self, idv, data_len, data):
        """Make a frame"""
        return np.concatenate(self.preamble, np.packbits(hamming), data)

    def syndrome(self, bits):
        """Compute the syndrome (check Hamming code) for an unpacked array of 31 bits"""
        assert(len(bits) == 31)
        return reduce(op.xor, [i for i, bit in enumerate(bits) if bit])

    def general_work(self, input_items, output_items):
        """
        This block has no inputs or output 
        """
        return 0;

