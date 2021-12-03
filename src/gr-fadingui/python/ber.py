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


import numpy as np
from gnuradio import gr

from fadingui.logger import get_logger
log = get_logger("ber")

class ber(gr.sync_block):
    """
    docstring for block ber
    """
    def __init__(self, vgl, vlen):
        gr.sync_block.__init__(self,
            name="ber",
            in_sig=[np.dtype(str(vlen) + "b")],
            out_sig=None)
        self.vgl=vgl
        self.vlen=vlen

    def work(self, input_items, output_items):
        
        inp = input_items[0]
        ber_tot = 0
        log.debug(f"Length: {len(inp)}")
        log.debug(f"Inp_vector:{inp}")
        
        for i in inp:
            log.debug(f"In Schlaufe{i}")
            v = np.array(self.vgl, dtype=np.uint8)^np.array(i, dtype=np.uint8)
            ber = sum(np.unpackbits(v))
            log.debug(f"BER {ber} in Paket {i}")
            ber_tot+=ber
            log.debug(f"BER Total{ber_tot}")
        

        return len(input_items[0])

