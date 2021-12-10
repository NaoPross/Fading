import numpy as np
from gnuradio import gr

# remove print for now
print = lambda x: None

np.set_printoptions(formatter={'int':hex})

class blk(gr.sync_block):
    def __init__(self, vlen=1):
        dt = np.byte if vlen == 1 else (np.byte, vlen)

        gr.sync_block.__init__(
            self,
            name='Printer',
            in_sig=[(np.byte, vlen)],
            out_sig=[]
        )

    def work(self, input_items, output_items):
        inp = np.array(input_items[0], dtype=np.uint8)
        print(f"Decoded {len(inp)} samples:\n{inp}")

        return len(inp)
