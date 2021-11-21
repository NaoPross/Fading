#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Naoki Pross.

import numpy as np
from gnuradio import gr

class deframer(gr.sync_block):
    """
    Check for integrity and remove frame header from packet.
    """
    def __init__(self, frame_obj):
        gr.sync_block.__init__(self,
            name="deframer",
            in_sig=[np.byte],
            out_sig=[np.byte])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        out[:] = in0
        return len(output_items[0])

