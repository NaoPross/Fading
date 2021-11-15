#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Naoki Pross, Sara Halter.
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

import io

import numpy as np
from gnuradio import gr

class datasource(gr.sync_block):
    """
    Loads data from a file choosen in the graphical user interface.
    """
    def __init__(self, vec_len, sock_addr, file_list):
        gr.sync_block.__init__(self,
            name="datasource",
            in_sig=None,
            out_sig=[np.dtype('{vec_len}b')])

        # parameters
        self.header_size = 11
        self.vec_len = vec_len
        self.sock_addr = sock_addr
        self.file_list = file_list

        # file members
        self.fdata = None
        self.fsize = None
        self.fpos = 0

        # TODO: make it possible to choose from UI
        self.load_file(file_list[0])

    def load_file(self, fname):
        self.fdata = np.fromfile(fname, np.byte)
        self.fsize = len(self.data)

        # TODO: remove debugging statements
        print(f"datasource: loaded file size={self.fsize}, head:")
        print(self.fdata[:10])

    def make_frame(self, data_size):
        # TODO: check that data_size is not too big
        pilot = 0x1248
        header = f"p{pilot:04x}s{data_size:04x}d".encode("ascii")
        arr = np.array(bytearray(header))

        assert(len(arr) == self.header_size)
        return arr

    def work(self, input_items, output_items):
        out = output_items[0]

        if self.fpos + self.vec_len > self.fsize:
            rest = self.fsize - self.fpos

            out[:rest] = self.fdata[self.fpos:rest]
            out[rest:] = 0 # TODO: replace with 01010101.. seq or scramble

            self.fpos = 0
            return 0

        out[:] = self.fdata[self.fpos:self.fpos + self.vec_len]
        self.fpos += self.vec_len

        return len(output_items[0])

