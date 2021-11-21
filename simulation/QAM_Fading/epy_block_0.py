"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, amplitudes=[], delays=[]):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.amplitues = amplitudes
        self.delays = delays

        #self.fir = 

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        inp = input_items[0]
        oup = output_items[0]
        amplitudes = [0.2, 0.5 ,0.8]
        delays = [3,5,2]
        i = len(amplitudes)

        outp[:] = [([1]+[0 for n in range (0,delays[i])]+[amplitudes[i]]) for i in range(0,i)]

        return len(output_items[0])


if __name__ == '__main__':
    ampl = [0.2, 0.5 ,0.8]
    delays = [3,5,2]
    i = len(ampl)
    [([1]+[0 for n in range (0,delays[i])]+[ampl[i]]) for i in range(0,i)]


