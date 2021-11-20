#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Naoki Pross.

from functools import reduce
import operator as op

import numpy as np
from gnuradio import gr


class frame_obj:
    """
    Frame Object: Contains informations about a data frame.

      -------------------------------------------------------------------------------
      | Preamble | Padding | ID     | Data Length | Parity | Payload | Padding      |
      | k bytes  | 1 bit   | 5 bits | 21 bits     | 5 bits |         | if necessary |
      -------------------------------------------------------------------------------
                           | (31, 26) Hamming EC code      |
                           ---------------------------------

    - The preamble is user defined.
    - The ID (5 bits) + Data length (21 bits) together are a 26 bits, followed
      by 5 parity bits computed using a (31,26) hamming code.

      This constraints the maximum payload size to 2 MiB and the number IDs to
      32, i.e. max file size is 64 MiB.

    """
    def __init__(self, preamble, payload_len):
        self._preamble = np.array(preamble, dtype=np.uint8)

        self._preamble_len = len(self._preamble)
        self._payload_len = payload_len

    @property
    def header_length(self) -> int:
        """Get header length in bytes"""
        # 4 is the number of bytes for the hamming part
        return self._preamble_len + 4

    @property
    def payload_length(self) -> int:
        return self._payload_len

    @property
    def length(self) -> int:
        """Get frame lenght in bytes"""
        # 8 is the size of the hamming ECC part + 1 bit
        return self.header_length + self.payload_length

    @property
    def preamble(self):
        """Get preamble"""
        return self._preamble

    def parity(self, bits):
        """Compute the 5 parity bits for an unpacked array of 26 bits"""
        assert(len(bits) == 26)
        # FIXME: does not work
        # return np.matmul(bits, gen) % 2
        return np.array([0, 0, 0, 0, 0])

    def make(self, idv, data_len, data):
        """Make a frame"""
        # get lower 4 bits of idv
        idv_bits = np.unpackbits([np.uint8(idv)])[:5]

        # get lower 22 bits of data_len
        data_len_bytes = list(map(np.uint8, data_len.to_bytes(4, byteorder='little')))
        data_len_bits = np.unpackbits(data_len_bytes)[:21]

        # compute 5 parity bits
        metadata = np.concatenate([idv_bits, data_len_bits])
        parity_bits = self.parity(metadata)

        # add padding
        hamming_bits = np.concatenate([[0], metadata, parity_bits])
        assert(len(hamming_bits) == 32)

        # pack 32 bits into 4 bytes and add the rest
        hamming = np.packbits(hamming_bits)
        return np.concatenate([self.preamble, hamming, data])

    def syndrome(self, bits):
        """Compute the syndrome (check Hamming code) for an unpacked array of 31 bits"""
        assert(len(bits) == 31)
        return reduce(op.xor, [i for i, bit in enumerate(bits) if bit])

