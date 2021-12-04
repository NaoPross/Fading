"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

np.set_printoptions(formatter={'int':hex})

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Printer',
            in_sig=[np.byte],
            out_sig=[]
        )

    def work(self, input_items, output_items):
        inp = np.array(input_items[0], dtype=np.uint8)
        print(f"Decoded {len(inp)} samples:\n{inp}")

        return len(inp)
