#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Naoki Pross.

import pmt

import numpy as np
from gnuradio import gr

import fadingui.logger

from fadingui.logger import get_logger
log = get_logger("phasecorrection")

class phasecorrection(gr.sync_block):
    """
    Apply phase and frequency correction where there is a correlation peak tag.

    The correlation peak tags are NOT propagated, and instead replaced with a
    frame_start tag.
    """
    def __init__(self, frame_len):
        gr.sync_block.__init__(
            self,
            name='Phase and Frequency Correction',
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )

        # tags should not be propagated, we then output our own tags
        self.set_tag_propagation_policy(gr.TPP_DONT)

        # save frame length
        self.frame_len = frame_len

        # because we do block processing, we need to keep track of the last tag
        # of the previous block to correct the first values of the next block
        self.last = None
        self.lastfreq = 0

        # debugging variables to check if an error happened in block processing
        self.lastnsamples = 0
        self.lastnback = 0

    def block_phase(self, start, end):
        """
        Compute a vector for the phase and frequency correction for the samples
        between two tags (start and end).

        @param start Tag where the samples should start to be corrected
        @param end   Tag where to stop correcting

        @return A vector of phase values for each sample. To correct the samples
                the data should be multiplied with np.exp(-1j * phase)
        """
        # compute number of samples between tags
        nsamples = end.offset - start.offset

        # debugging, see last lines of self.work()
        self.lastnsamples = nsamples

        # unpack pmt values into start and end phase
        sphase = pmt.to_python(start.value)
        ephase = pmt.to_python(end.value)

        # compute frequency offset between start and end
        phasediff = (ephase - sphase) % (2 * np.pi)
        freq = phasediff / nsamples

        if freq < 1e-3:
            freq = 0

        # save this one for the last block (see variable `end' in self.work)
        self.lastfreq = freq

        # debugging
        log.debug(f"Correction for chunk of {nsamples:2d} samples is " \
              f"sphase={sphase: .4f} rad, ephase={ephase: .4f} rad and freq={freq*1e3: .4f}e-3 rad / sample")
        self.lastnsamples = nsamples

        # compute chunk values
        return sphase * np.ones(nsamples) + freq * np.arange(0, nsamples)

    def work(self, input_items, output_items):
        counter = self.nitems_written(0)
        log.debug(f"Counter is at {counter} (nitems_written)")

        # nicer aliases
        inp = input_items[0]
        out = output_items[0]

        # read phase tags
        is_phase = lambda tag: pmt.to_python(tag.key) == "phase_est"
        tags = list(filter(is_phase, self.get_tags_in_range( \
                0, counter, counter + len(inp))))

        if not tags:
            log.warning(f"There were no tags in {len(inp)} samples!")
            out[:] = inp
            return len(out)

        # debugging
        log.debug(f"Processing {len(tags)} tags = {tags[-1].offset - tags[0].offset} " \
              f"samples out of {len(inp)} input samples")

        # compute "the middle"
        enough_samples = lambda pair: ((pair[1].offset - pair[0].offset) > 0)
        pairs = list(filter(enough_samples, zip(tags, tags[1:])))
        chunks = [ self.block_phase(start, end) for (start, end) in pairs ]
        middle = np.concatenate(chunks) if chunks else []

        # compute values at the end, we do not have informations about the future
        # but we can use the frequency of the last tag to approximate
        nback = len(inp) - (tags[-1].offset - counter)
        log.debug(f"Processing {nback} samples at the back of the buffer")
        end = np.ones(nback) * pmt.to_python(tags[-1].value) \
                + self.lastfreq * np.arange(0, nback)

        # compute the "start", using the last tag from the previous call
        nfront = tags[0].offset - counter
        log.debug(f"Processing {nfront} samples at the front of the buffer")
        start = self.block_phase(self.last, tags[0])[-nfront:] \
                if self.last and nfront else np.zeros(nfront)

        # debugging
        if self.lastnback + nfront != self.lastnsamples:
            log.warn("Something went wrong during block processing! " \
                    f"Last block finished with nback = {self.lastnback} samples, " \
                    f"current block starts with nfront = {nfront}, but their sum " \
                    f"is not {self.lastnsamples} = size of last chunk")
        self.lastnback = nback

        # compute correction
        correction = np.exp(-1j * np.concatenate([start, middle, end]))
        length = len(correction)

        # write outputs
        out[:] = inp * correction

        # save last tag for next call
        self.last = tags[-1]

        # add frame_start tags
        is_start = lambda tag: pmt.to_python(tag.key) == "corr_start"
        start_tags = list(filter(is_start, \
                self.get_tags_in_range(0, counter, counter + len(inp))))
        for tag in start_tags:
            self.add_item_tag(0, tag.offset +1, pmt.intern("frame_start"), \
                    pmt.from_long(self.frame_len))

        return len(out)
