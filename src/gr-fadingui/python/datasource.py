#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Naoki Pross.

import io

import numpy as np
from gnuradio import gr

class datasource(gr.sync_block):
    """
    Loads data from a file choosen in the graphical user interface, splits into
    chunks and puts a preamble in front of it(frame).
    """

    HEADER_LEN = 11;

    def __init__(self, vec_len, header_len, sock_addr, file_list):
        # FIXME: find a better solution
        assert(header_len == datasource.HEADER_LEN)

        gr.sync_block.__init__(self,
            name="datasource",
            in_sig=None,
            out_sig=[np.dtype(f'{vec_len + header_len}b')])

        # parameters
        self.vec_len = vec_len
        self.sock_addr = sock_addr
        self.file_list = file_list

        # file members
        self.fdata = None
        self.fsize = None
        self.fpos = 0

        # cache
        self.header_cache = None

        # TODO: make it possible to choose from UI
        self.load_file(file_list[0])

    def load_file(self, fname):
        self.fdata = np.fromfile(fname, np.byte)
        self.fsize = len(self.fdata)

        # TODO: remove debugging statements or create logger
        print(f"datasource: loaded file size={self.fsize}, head:")
        print(self.fdata[:10])

    def make_header(self, data_size):
        # TODO: check that data_size is not too big
        pilot = 0x1248

        # TODO: implement hamming code for header
        header = f"p{pilot:04x}s{data_size:04x}d".encode("ascii")

        arr = np.frombuffer(header, dtype=np.dtype("byte"))
        return arr

    def work(self, input_items, output_items):
        out = output_items[0]

        if self.fpos + self.vec_len > self.fsize:
            # FIXME: repair broken code below
            # TODO: create logger
            print(f"WARNING: the last {self.fsize - self.fpos} bytes were not sent!")
            self.fpos = 0
            return 0;

            rest = self.fsize - self.fpos

            # cannot use cached header
            header = self.make_header(rest)
            data = self.fdata[self.fpos:rest]

            frame_size = datasource.HEADER_LEN + rest
            out[:] = np.concatenate([header, data])

            self.fpos = 0
            return rest

        # cache header if not saved
        if self.header_cache == None:
            self.header = self.make_header(self.vec_len)

        data = self.fdata[self.fpos:self.fpos + self.vec_len]

        out[:] = np.concatenate([self.header, data])

        self.fpos += self.vec_len
        return len(output_items[0])

