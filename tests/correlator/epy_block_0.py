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

        # we need to keep track of the aboslute number of samples that have
        # been processed, because tags have an absolute offset
        self.counter: np.uint64 = 0

        # because we do block processing, we need to keep track of the last tag
        # of the previous block to correct the first values of the next block
        self.last = None

        # both the phase and frequency corrections should go through a low pass
        # filter to avoid werid jumps in the correction. to do that, there are
        # two buffers with an index
        self.index = 0
        self.length = 7
        self.freq = np.zeros(self.length)

    def lpf_freq(self, new_sample):
        # save new sample
        self.freq[self.index] = new_sample
        # increment index
        self.index = (self.index + 1) % self.length

        return np.sum(self.freq) / self.length

    def block_phase(self, start, end):
        # compute number of samples in block
        nsamples = end.offset - start.offset

        # unpack pmt values into start and end phase
        sphase = pmt.to_python(start.value)
        ephase = pmt.to_python(end.value)

        # compute frequency offset between start and end
        # and run it through a low pass filter (mean)
        freq = (sphase - ephase) / nsamples
        freq = self.lpf_freq(freq)

        # debugging
        print(f"Correction for block of {nsamples:2d} samples is " \
              f"phase={sphase: .4f} rad and freq={freq*1e3: .4f} milli rad / sample")

        # compute block values
        return sphase * np.ones(nsamples) + freq * np.arange(0, nsamples)

    def work(self, input_items, output_items):
        # FIXME: replace class counter with local variable
        self.counter = self.nitems_written(0)

        # nicer aliases
        inp = input_items[0]
        out = output_items[0]

        # read phase tags
        is_phase = lambda tag: pmt.to_python(tag.key) == "phase_est"
        tags = list(filter(is_phase, self.get_tags_in_window(0, 0, len(inp))))

        if not tags:
            print(f"There were no tags in {len(inp)} samples!")
            out[:] = inp
            return len(out)

        # debugging
        print(f"Processing {len(tags)} tags = {tags[-1].offset - tags[0].offset} " \
              f"samples out of {len(inp)} input samples")

        # compute "the middle"
        enough_samples = lambda pair: ((pair[1].offset - pair[0].offset) > 0)
        pairs = list(filter(enough_samples, zip(tags, tags[1:])))
        blocks = [ self.block_phase(start, end) for (start, end) in pairs ]
        middle = np.concatenate(blocks) if blocks else []

        # compute values at the end, we do not have informations about the future
        # but we can use the frequency of the last block to approximate
        nback = len(inp) - (tags[-1].offset - self.counter)
        print(f"Processing {nback} samples at the back of the buffer")
        endfreq = self.lpf_freq(self.freq[-1])
        end = np.ones(nback) * pmt.to_python(tags[-1].value) + endfreq * np.arange(0, nback)

        # compute the "start", using the last tag from the previous call
        nfront = tags[0].offset - self.counter
        print(f"Processing {nfront} samples at the front of the buffer")
        start = self.block_phase(self.last, tags[0])[-nfront:] \
                if self.last and nfront else np.zeros(nfront)

        # compute correction
        correction = np.exp(-1j * np.concatenate([start, middle, end]))
        length = len(correction)

        # write outputs
        out[:length] = inp[:length] * correction
        self.counter += len(inp)

        # save last tag for next call
        self.last = tags[-1]

        # FIXME: should return `length' but then the last sample is not
        #        included and self.last does something weird
        return len(out)
