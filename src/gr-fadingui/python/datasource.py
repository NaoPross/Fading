#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Naoki Pross.

import io

import numpy as np
from gnuradio import gr

from fadingui.logger import get_logger
log = get_logger("datasource")


class datasource(gr.basic_block):
    """
    Loads data from a file choosen splits into chunks and pack them into
    frames.
    """

    def __init__(self, frame_obj, filename):
        gr.basic_block.__init__(self,
            name="datasource",
            in_sig=None,
            out_sig=[np.byte])

        # Frame object
        self.frame = frame_obj

        # file members
        self.fname = filename
        self.fdata = np.fromfile(self.fname, np.byte)
        self.fsize = len(self.fdata)

        # a frame has 5 id bits so, there can only be 2 ** 5 chunks per file
        # see docstring of frame_obj for more details
        nblocks = int(self.fsize / self.frame.payload_length)
        log.debug(f"Loaded {self.fsize} bytes = {nblocks} blocks from name={self.fname}")
        assert nblocks < 2 ** 5, "Payload size too small or file too big"

        self.fpos = 0
        self.blocknr = 0

        # would have been nice to have but does not work
        # self.set_min_noutput_items(frame_obj.length)

        # FIXME: implement buffering
        # output buffer
        self.outbuffer = np.array([])

    def general_work(self, input_items, output_items):
        out = output_items[0]


        # FIXME: if there is leftover buffer add that first
        # if self.outbuffer.size > 0:
        #     log.debug("Frame did not fit into buffer")
        #     out[:len(self.outbuffer)] = self.outbuffer

        if self.fpos + self.frame.payload_length > self.fsize:
            # FIXME: implement edge case
            log.warning(f"The last {self.fsize - self.fpos} bytes were not sent!")
            self.fpos = 0
            self.blocknr = 0

            log.debug("File finished, starting over")
            return 0;

        data = self.fdata[self.fpos:self.fpos + self.frame.payload_length]
        frame_bytes = self.frame.make(self.blocknr, self.frame.payload_length, data)

        out[:] = frame_bytes[:len(out)]
        self.outbuffer = frame_bytes[len(out):]

        log.debug(f"Sent frame nr={self.blocknr}")
        log.debug(f"Set bytes {out}")

        self.fpos += self.frame.payload_length
        self.blocknr += 1

        return self.frame.length

