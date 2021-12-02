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
        self.last_phase = 0

    def work(self, input_items, output_items):
        # TODO: interpolate phase values for frequency correction

        out = output_items[0]
        inp = input_items[0]

        # create a phase correction vector
        phase = np.zeros(len(inp), dtype=np.float64)

        # read tags
        tags = self.get_tags_in_window(0, 0, len(inp))

        # get only phase tags
        is_phase = lambda tag: pmt.to_python(tag.key) == "phase_est"
        phase_tags = list(filter(is_phase, tags))

        print(f"Processing {len(inp)} samples, with {len(phase_tags)} tags")

        # compute correction from previous block
        first_tag = phase_tags[0]
        first_idx = first_tag.offset - self.sampnr
        phase[:first_idx] = self.last_phase

        # iterate phase tags "in the middle"
        for prev_tag, next_tag in zip(phase_tags, phase_tags[1:]):
            # unpack pmt values
            pval = pmt.to_python(prev_tag.value)

            # compute indexes in phase vector
            pidx = prev_tag.offset - self.sampnr
            idx = next_tag.offset - self.sampnr

            # compute phase correction for block
            phase[pidx:idx] = pval
            print(f"Correction for block {pidx} to {idx} is {pval}")

        # compute the remaining part of the block
        last_tag = phase_tags[-1]
        last_val = pmt.to_python(last_tag.value)
        last_idx = last_tag.offset - self.sampnr

        phase[last_idx:] = last_val

        # save values for next call
        self.last_phase = last_val

        # mark samples as processed and compute to output
        self.sampnr += len(inp)
        out[:] = inp * np.exp(-1j * phase)

        return len(out)
