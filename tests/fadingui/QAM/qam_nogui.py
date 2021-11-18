#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: QAM
# Author: Pross Naoki, Halter Sara Cinzia
# GNU Radio version: 3.8.2.0

from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import fadingui


class qam_nogui(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "QAM")

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.nfilts = nfilts = 32
        self.excess_bw = excess_bw = 350e-3
        self.variable_4 = variable_4 = 0
        self.timing_loop_bw = timing_loop_bw = 2 * 3.141592653589793 / 100
        self.time_offset = time_offset = 1
        self.samp_rate = samp_rate = 32000
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), excess_bw, 45*nfilts)
        self.qam_const = qam_const = digital.constellation_rect([(-3-3j), (-1-3j), (1-3j), (3-3j), (-3-1j), (-1-1j), (1-1j), (3-1j), (-3+1j), (-1+1j), (1+1j), (3+1j), (-3+3j), (-1+3j), (1+3j), (3+3j)], [0, 4, 12, 8, 1, 5, 13, 9, 3, 7, 15, 11, 2, 6, 14, 10],
        4, 1, 1, 1, 1).base()
        self.phase_bw = phase_bw = 2 * 3.141592653589793 / 100
        self.noise_volt = noise_volt = 100e-6
        self.freq_offset = freq_offset = 0
        self.eq_ntaps = eq_ntaps = 15
        self.eq_mod = eq_mod = 1
        self.eq_gain = eq_gain = 10e-3
        self.const = const = digital.constellation_16qam().base()
        self.chn_taps = chn_taps = [1.0 + 0.0j, ]

        ##################################################
        # Blocks
        ##################################################
        self.fadingui_xor_frame_sync_0 = fadingui.xor_frame_sync(sync_pattern=[], buffer_size=128)
        self.fadingui_dearpygui_sink_0 = fadingui.dearpygui_sink(sock_addr='udp://localhost:31415', ui_element_id=0)
        self.fadingui_datasource_0 = fadingui.datasource(vec_len=2037, header_len=11, sock_addr='udp://', file_list=["./lena512color.tiff"])
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, timing_loop_bw, rrc_taps, nfilts, nfilts/2, 1.5, 1)
        self.digital_map_bb_0 = digital.map_bb([0, 1, 3, 2])
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(4)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(phase_bw, 4, False)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=const,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=excess_bw,
            verbose=False,
            log=False)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(const)
        self.digital_cma_equalizer_cc_0 = digital.cma_equalizer_cc(eq_ntaps, eq_mod, eq_gain, 1)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise_volt,
            frequency_offset=freq_offset,
            epsilon=time_offset,
            taps=chn_taps,
            noise_seed=0,
            block_tags=False)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_char*1, 2048)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.fadingui_dearpygui_sink_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.fadingui_xor_frame_sync_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_cma_equalizer_cc_0, 0))
        self.connect((self.fadingui_datasource_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.fadingui_xor_frame_sync_0, 0), (self.blocks_null_sink_0, 0))


    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 45*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 45*self.nfilts))

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 45*self.nfilts))

    def get_variable_4(self):
        return self.variable_4

    def set_variable_4(self, variable_4):
        self.variable_4 = variable_4

    def get_timing_loop_bw(self):
        return self.timing_loop_bw

    def set_timing_loop_bw(self, timing_loop_bw):
        self.timing_loop_bw = timing_loop_bw
        self.digital_pfb_clock_sync_xxx_0.set_loop_bandwidth(self.timing_loop_bw)

    def get_time_offset(self):
        return self.time_offset

    def set_time_offset(self, time_offset):
        self.time_offset = time_offset
        self.channels_channel_model_0.set_timing_offset(self.time_offset)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.rrc_taps)

    def get_qam_const(self):
        return self.qam_const

    def set_qam_const(self, qam_const):
        self.qam_const = qam_const

    def get_phase_bw(self):
        return self.phase_bw

    def set_phase_bw(self, phase_bw):
        self.phase_bw = phase_bw
        self.digital_costas_loop_cc_0.set_loop_bandwidth(self.phase_bw)

    def get_noise_volt(self):
        return self.noise_volt

    def set_noise_volt(self, noise_volt):
        self.noise_volt = noise_volt
        self.channels_channel_model_0.set_noise_voltage(self.noise_volt)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.channels_channel_model_0.set_frequency_offset(self.freq_offset)

    def get_eq_ntaps(self):
        return self.eq_ntaps

    def set_eq_ntaps(self, eq_ntaps):
        self.eq_ntaps = eq_ntaps

    def get_eq_mod(self):
        return self.eq_mod

    def set_eq_mod(self, eq_mod):
        self.eq_mod = eq_mod
        self.digital_cma_equalizer_cc_0.set_modulus(self.eq_mod)

    def get_eq_gain(self):
        return self.eq_gain

    def set_eq_gain(self, eq_gain):
        self.eq_gain = eq_gain
        self.digital_cma_equalizer_cc_0.set_gain(self.eq_gain)

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def get_chn_taps(self):
        return self.chn_taps

    def set_chn_taps(self, chn_taps):
        self.chn_taps = chn_taps
        self.channels_channel_model_0.set_taps(self.chn_taps)





def main(top_block_cls=qam_nogui, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
