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
        log.debug(los) #TO DO: True False unterscheidung 
        if los == True:
            self.los = 1
            log.debug("Los True")
        else: 
            self.los = 0
            log.debug("Los False")


        
        

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        inp = input_items[0]
        oup = output_items[0]
        
        if len(self.amplitudes) != len(self.delays):    # Test: Es muss gleich viele Werte für Delays und Amplituden haben.
            raise Exception("Amplitudes and Delay length dont match")


        #TO DO negativ check 

        

        #    raise Exception("Delay length can't be one")
        #if np.min(self.delays)<=1:
        #    raise Exception("Delay length can't be one")

        #max_len = np.max(self.delays) #Max Werte herausfinden für länge 
        #sum_x = np.zeros(max_len)

        max_order = 2 * np.floor(np.max(self.delays)) + 1
        max_samples = np.arange(0, max_order +1) 
        max_len = len(max_samples) #Für Filter

        sum_x = np.zeros(int(max_len))

        for (a,d) in zip(self.amplitudes,self.delays):
            # if d-1 <= 0:
            #     x = np.concatenate([[a], np.zeros(max_len-1)])
            # else:    
            order = 2 * np.floor(d) + 1

            skip = np.floor(d) - (order - 1) / 2 #M sollte immer 0 sein 
            assert skip >= 0

            samples = np.arange(0, order +1)  

            h = a*(np.sinc(samples-d)) #sinc
            h_len = np.concatenate([h, np.zeros(max_len-len(h))])

            sum_x += h_len

            #x = np.concatenate([np.zeros(d-1), [a], np.zeros(max_len-d)])
            #sum_x += x
        
        sum_x[0] = self.los
        #log.debug(sum_x)


        y = np.convolve(inp, sum_x)
        
        # signal_shifted = np.convolve(h, inp, mode='full')
        # y = signal_shifted

        #y+=np.concatenate([self.temp,np.zeros(len(y)-len(self.temp))])
        y+=np.concatenate([self.temp,np.zeros(len(y)-len(self.temp))])

        oup[:] = y[:len(inp)]
        self.temp = y[len(inp):]        
        

        return len(oup)