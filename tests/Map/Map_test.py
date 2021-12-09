#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Map test
# Author: Sara Halter
# GNU Radio version: 3.8.2.0

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import epy_block_1
import numpy as np


class Map_test(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Map test")

        ##################################################
        # Variables
        ##################################################
        self.v3 = v3 = 0.7071067811865475+0.7071067811865475j
        self.v2 = v2 = -0.7071067811865475+0.7071067811865475j
        self.v1 = v1 = 0.7071067811865475-0.7071067811865475j
        self.v0 = v0 = -0.7071067811865475-0.7071067811865475j
        self.samp_rate = samp_rate = 32000
        self.const = const = digital.constellation_16qam().base()
        self.a3 = a3 = -9.486832980505138-9.486832980505138j
        self.a2 = a2 = 9.486832980505138-9.486832980505138j
        self.a1 = a1 = -3.162277660168379-3.162277660168379j
        self.a0 = a0 = 3.162277660168379-3.162277660168379j

        ##################################################
        # Blocks
        ##################################################
        self.epy_block_1 = epy_block_1.blk()
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(const)
        self.blocks_vector_source_x_1_0 = blocks.vector_source_c([(-0.9486832980505138-0.31622776601683794j), (-0.9486832980505138-0.31622776601683794j)], True, 1, [])
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(2, 8, "", False, gr.GR_MSB_FIRST)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.epy_block_1, 0))
        self.connect((self.blocks_vector_source_x_1_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_repack_bits_bb_0, 0))


    def get_v3(self):
        return self.v3

    def set_v3(self, v3):
        self.v3 = v3

    def get_v2(self):
        return self.v2

    def set_v2(self, v2):
        self.v2 = v2

    def get_v1(self):
        return self.v1

    def set_v1(self, v1):
        self.v1 = v1

    def get_v0(self):
        return self.v0

    def set_v0(self, v0):
        self.v0 = v0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def get_a3(self):
        return self.a3

    def set_a3(self, a3):
        self.a3 = a3

    def get_a2(self):
        return self.a2

    def set_a2(self, a2):
        self.a2 = a2

    def get_a1(self):
        return self.a1

    def set_a1(self, a1):
        self.a1 = a1

    def get_a0(self):
        return self.a0

    def set_a0(self, a0):
        self.a0 = a0





def main(top_block_cls=Map_test, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
