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
from numpy.fft import fft,ifft,fftshift
from gnuradio import gr

from fadingui.logger import get_logger
log = get_logger("multipath_fading")

class multipath_fading(gr.sync_block):
    """
    docstring for block multipath_fading
    """
    def __init__(self, amplitudes, delays, los):
        gr.sync_block.__init__(
            self,
            name='Multipath fading',
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )

        if len(amplitudes) != len(delays):
            raise Exception("Amplitudes and Delay length dont match")

        if np.min(delays) < 0:
            raise Exception("Delay can't be negative")

        self.amplitudes = amplitudes
        self.delays = delays
        self.temp = [0]
        self.los = 1 if los else 0

    def work(self, input_items, output_items):
        inp = input_items[0]
        oup = output_items[0]

        max_order = 2 * np.floor(np.max(self.delays)) + 1
        max_samples = np.arange(0, max_order +1) 
        max_len = len(max_samples)

        tot_h = np.zeros(int(max_len))

        for (a, d) in zip(self.amplitudes, self.delays):
            order = 2 * np.floor(d) + 1
            samples = np.arange(0, order +1)
            # compute FIR
            h = a * np.sinc(samples - d)
            # adjust length
            h = np.concatenate([h, np.zeros(max_len - len(h))])
            tot_h += h

        tot_h[0] += self.los

        # compute output and add rest from last block processing
        y = np.convolve(inp, tot_h)
        y += np.concatenate([self.temp, np.zeros(len(y) - len(self.temp))])
        # write output
        oup[:] = y[:len(inp)]
        # save for next block processing
        self.temp = y[len(inp):]

        return len(oup)
