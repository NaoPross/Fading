import pmt

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Phase Lock',
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )

        # keep track of how many samples were processed,
        # because tags have an absolute offset
        self.sampnr: np.complex64 = 0

        # because of block processing a tagged block could
        # be split in half so we need to keep track of the
        # "previous" values
        self.last_tag = None

    def work(self, input_items, output_items):
        # nicer aliases
        out = output_items[0]
        inp = input_items[0]

        def print_phase_correction(start, end, phase, freq):
            print(f"Correction for block {start:3d} to {end:3d} is phase = {phase: 2.4f} rad, freq = {freq * 1e3: 2.4f} milli rad/samp")

        # read only phase tags
        tags = self.get_tags_in_window(0, 0, len(inp))

        is_phase = lambda tag: pmt.to_python(tag.key) == "phase_est"
        phase_tags = list(filter(is_phase, tags))

        # FIXME: what if there are no tags? check that!

        print(f"Processing {len(inp)} samples, with {len(phase_tags)} tags")

        # create a phase correction vector
        phase = np.zeros(len(inp), dtype=np.float64)

        # compute correction from previous block (if present)
        if self.last_tag:
            # variables for first and last phase values
            lval = pmt.to_python(self.last_tag.value)
            fval = pmt.to_python(phase_tags[0].value)

            # compute index for phase vector
            fidx = phase_tags[0].offset - self.sampnr

            # compute frequency offset
            nsamples = phase_tags[0].offset - self.last_tag.offset
            freq = (fval - lval) / nsamples

            # total phase correction is: phase + freq * time
            phase[:fidx] = lval * np.ones(fidx) + freq * np.arange(0, fidx)

            # compute correction
            print_phase_correction(0, fidx, lval, freq)

        # iterate phase tags "in the middle"
        # FIXME: what if there are less than 2 tags?
        #        the code below will probably crash
        for prev_tag, next_tag in zip(phase_tags, phase_tags[1:]):
            # unpack pmt values
            pval = pmt.to_python(prev_tag.value)
            nval = pmt.to_python(next_tag.value)

            # compute indexes in phase vector
            pidx = prev_tag.offset - self.sampnr
            nidx = next_tag.offset - self.sampnr

            # compute frquency correction for block by linearly interpolating
            # frame values
            nsamples = nidx - pidx
            freq = (nval - pval) / nsamples

            # total correction is: phase + freq * time
            phase[pidx:nidx] = pval * np.ones(nsamples) + freq * np.arange(0, nsamples)
            print_phase_correction(pidx, nidx, pval, freq)

        # for the last block because the next tag is unknown (in the future) we
        # cannot predict the frequency offset. Thus we save the last tag for
        # the next call.
        self.last_tag = phase_tags[-1]
        val = pmt.to_python(self.last_tag.value)
        idx = self.last_tag.offset - self.sampnr

        phase[idx:] = val

        # compute correction
        out[:] = inp * np.exp(-1j * phase)

        # increment processed samples counter
        self.sampnr += len(inp)
        return len(phase)
