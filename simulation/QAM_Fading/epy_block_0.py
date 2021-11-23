"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from numpy.fft import fft,ifft,fftshift
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, amplitudes=[], delays=[], los=True):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.amplitudes = amplitudes
        self.delays = delays
        self.temp = [0]
        # if los:
        #     self.amplitudes.append(1)
        #     self.delays.append(0)
        self.los= 1
        #self.fir = 

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        inp = input_items[0]
        oup = output_items[0]
        
        if len(self.amplitudes) != len(self.delays):
            raise Exception("Amplitudes and Delay length dont match")

        #    raise Exception("Delay length can't be one")
        #if np.min(self.delays)<=1:
        #    raise Exception("Delay length can't be one")
        max_len = np.max(self.delays)
        sum_x = np.zeros(max_len)
        for(a,d) in zip(self.amplitudes,self.delays):
            # if d-1 <= 0:
            #     x = np.concatenate([[a], np.zeros(max_len-1)])
            # else:                
            x = np.concatenate([np.zeros(d-1), [a], np.zeros(max_len-d)])
            sum_x += x
        
        #sum_x[0] = self.los
        print(sum_x)
        
        H_int = fft(sum_x)

        h = ifft(H_int)

        #h[0]=1

        y = np.convolve(inp, sum_x)
        
        y+=np.concatenate([self.temp,np.zeros(len(y)-len(self.temp))])
        

        oup[:] = y[:len(inp)]
        self.temp = y[len(inp):]        
        

        return len(oup)