import pmt
import numpy as np
from gnuradio import gr


class blk(gr.sync_block):

    def __init__(self, tag="frame_start", vlen=1):
        dt = np.byte if vlen == 1 else (np.byte, vlen)

        gr.sync_block.__init__(
            self,
            name='Split at tag',
            in_sig=[np.byte],
            out_sig=[(np.byte, vlen)]
        )

        self.tag = tag
        self.vlen = vlen

    def work(self, input_items, output_items):
        inp = input_items[0]

        is_frame_start = lambda tag: pmt.to_python(tag.key) == self.tag
        tags = filter(is_frame_start, self.get_tags_in_window(0, 0, len(inp)))

        counter = self.nitems_written(0)
        offsets = map(lambda t: t.offset - counter, tags)

        print(list(offsets))

        output_items[0][:] = inp
        return len(output_items[0])
