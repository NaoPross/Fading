#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Naoki Pross.


import numpy
from gnuradio import gr

class xor_frame_sync(gr.sync_block):
    """
    docstring for block xor_frame_sync
    """
    def __init__(self, sync_pattern):
        gr.sync_block.__init__(self,
            name="xor_frame_sync",
            in_sig=[np.byte],
            out_sig=[np.byte])

    def work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]

        out[:] = inp

        return len(output_items[0])

