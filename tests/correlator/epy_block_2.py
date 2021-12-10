import pmt
import functools

import numpy as np
from gnuradio import gr


class blk(gr.decim_block):

    def __init__(self, tag="frame_start", vlen=1):
        decim = vlen

        gr.decim_block.__init__(
            self,
            name='Split at tag',
            in_sig=[np.byte],
            out_sig=[(np.byte, vlen)],
            decim = decim -1
        )

        if decim > 1:
            self.set_relative_rate(1. / (decim -1))

        self.tag = tag
        self.vlen = vlen

    def work(self, input_items, output_items):
        # nicer aliases
        inp = input_items[0]
        inplen = len(inp)
        oup = output_items[0]
        ouplen = len(oup)

        is_frame_start = lambda tag: pmt.to_python(tag.key) == self.tag
        tags = list(filter(is_frame_start, self.get_tags_in_window(0, 0, inplen)))

        if len(tags) == 0:
            print("There are not tags!")

        # get indices of where the frames are
        counter = self.nitems_written(0) # * self.vlen
        offsets = list(map(lambda t: t.offset - counter, tags))
        indices = list(zip(offsets, offsets[1:]))

        print(list(map(lambda t: t.offset, tags)))
        print(offsets)
        print(indices)

        # Get chunks
        def get_inp_chunk(index_pair): 
            # read a chunk from the inp array
            # if there are not enough values the rest is padded with zeros,
            # if there are too many values, they get cut off
            start = index_pair[0]
            end = index_pair[1]
            length = end - start

            assert start != end

            print(f"getting chunk from {start} to {end} of length {length}")

            # not enough values
            if length < self.vlen:
                pad = self.vlen - length
                print(f"Chunk was too short! Adding {pad} zeros to pad")
                return np.concatenate([inp[start:end], np.zeros(pad)])

            # too many values
            if length > self.vlen:
                print(f"Chunk was too long! Cutting off {length - self.vlen} values")
                end = start + self.vlen
                return inp[start:end]

            # okay
            rv = inp[start:end]
            print(rv)
            return rv

        chunks = list(map(get_inp_chunk, indices))

        assert len(chunks) != 0

        print(chunks)
        oup[:] = np.concatenate(chunks).reshape((-1, self.vlen))

        return len(oup)
