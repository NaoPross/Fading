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
    def __init__(self, amplitudes=[], delays=[], los=True):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.amplitudes = amplitudes
        self.delays = delays
        self.temp = [0]
        # if los:
        #     self.amplitudes.append(1)
        #     self.delays.append(0)
        self.los= 1
        #self.fir = 

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        inp = input_items[0]
        oup = output_items[0]
        
        if len(self.amplitudes) != len(self.delays):
            raise Exception("Amplitudes and Delay length dont match")

        #    raise Exception("Delay length can't be one")
        #if np.min(self.delays)<=1:
        #    raise Exception("Delay length can't be one")
        max_len = np.max(self.delays)
        sum_x = np.zeros(max_len)
        for(a,d) in zip(self.amplitudes,self.delays):
            # if d-1 <= 0:
            #     x = np.concatenate([[a], np.zeros(max_len-1)])
            # else:                
            x = np.concatenate([np.zeros(d-1), [a], np.zeros(max_len-d)])
            sum_x += x
        
        sum_x[0] = self.los
        log.debug(sum_x)
        
        #H_int = fft(sum_x)

        #h = ifft(H_int)

        #h[0]=1

        y = np.convolve(inp, sum_x)
        
        y+=np.concatenate([self.temp,np.zeros(len(y)-len(self.temp))])
        

        oup[:] = y[:len(inp)]
        self.temp = y[len(inp):]        
        

        return len(oup)