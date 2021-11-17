#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Naoki Pross.

import socket
from urllib.parse import urlparse

import numpy as np
from gnuradio import gr

class dearpygui_sink(gr.sync_block):
    """
    DearPyGUI Sink
    """
    def __init__(self, sock_addr, ui_element_id):
        gr.sync_block.__init__(self,
            name="dearpygui_sink",
            in_sig=[np.complex64],
            out_sig=None)

        # sockets
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.srv = urlparse(sock_addr)

    def send(self, value):
        data = value.tobytes()
        sent = self.socket.sendto(data, (self.srv.hostname, self.srv.port))

        return len(data) == sent

    def work(self, input_items, output_items):
        in0 = input_items[0]
        self.send(in0)
        return len(input_items[0])

