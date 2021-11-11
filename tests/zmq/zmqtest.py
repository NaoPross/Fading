#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: ZMQ test
# Author: Naoki Pross
# GNU Radio version: 3.8.2.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq


class zmqtest(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "ZMQ test")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_req_source_0 = zeromq.req_source(gr.sizeof_gr_complex, 1, '', 100, False, -1)
        self.zeromq_rep_sink_0 = zeromq.rep_sink(gr.sizeof_gr_complex, 1, '', 100, False, -1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.zeromq_rep_sink_0, 0))
        self.connect((self.zeromq_req_source_0, 0), (self.blocks_throttle_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)





def main(top_block_cls=zmqtest, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")
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
