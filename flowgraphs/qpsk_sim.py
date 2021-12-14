#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: QPSK Sim
# Author: Naoki Sean Pross, Sara Cinzia Halter
# GNU Radio version: 3.8.2.0

from gnuradio import blocks
import numpy
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
import numpy as np


class qpsk_sim(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "QPSK Sim")

        ##################################################
        # Variables
        ##################################################
        self.testvec = testvec = [0x1f, 0x35] + [0x12, 0x48]
        self.sps = sps = 4
        self.nfilts = nfilts = 32
        self.excess_bw = excess_bw = 0.35
        self.samp_rate = samp_rate = 1e6
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), excess_bw, 45*nfilts)
        self.qpsk_const = qpsk_const = digital.constellation_qpsk().base()
        self.frame_len = frame_len = len(testvec) +4
        self.carrier_freq = carrier_freq = 2.4e9
        self.access_code_symbols = access_code_symbols = [(-0.7071067811865475-0.7071067811865475j), (0.7071067811865475-0.7071067811865475j), (0.7071067811865475+0.7071067811865475j), (0.7071067811865475+0.7071067811865475j), (-0.7071067811865475-0.7071067811865475j), (0.7071067811865475+0.7071067811865475j), (0.7071067811865475-0.7071067811865475j), (0.7071067811865475-0.7071067811865475j)]

        ##################################################
        # Blocks
        ##################################################
        self.fadingui_phasecorrection_0 = fadingui.phasecorrection(frame_len)
        self.fadingui_netsink_4 = fadingui.netsink(address='udp://localhost:31417', dtype="complex", vlen=1)
        self.fadingui_netsink_3 = fadingui.netsink(address='udp://localhost:31419', dtype="complex", vlen=1)
        self.fadingui_netsink_1 = fadingui.netsink(address='udp://localhost:31418', dtype="complex", vlen=1)
        self.fadingui_netsink_0_0 = fadingui.netsink(address='udp://localhost:31415', dtype="float", vlen=1)
        self.fadingui_netsink_0 = fadingui.netsink(address='udp://localhost:31416', dtype="complex", vlen=1)
        self.fadingui_ber_0 = fadingui.ber(vgl=list(np.zeros(frame_len)), vlen=frame_len,address='udp://localhost:31420')
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, 2 * np.pi / 100, rrc_taps, 32, 16, 1.5, 1)
        self.digital_corr_est_cc_0 = digital.corr_est_cc(access_code_symbols, 1, len(access_code_symbols) // 2, 0.9, digital.THRESHOLD_ABSOLUTE)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=qpsk_const,
            differential=False,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=excess_bw,
            verbose=False,
            log=False)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(qpsk_const)
        self.digital_cma_equalizer_cc_0 = digital.cma_equalizer_cc(15, 1, 2e-3, 1)
        self.channels_selective_fading_model_0 = channels.selective_fading_model( 8, ((2*carrier_freq)/(3*10e8))/samp_rate, False, 4.0, 21, (0,1.8), (1,0.12), 8 )
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=100e-3,
            frequency_offset=2e-3,
            epsilon=1.0,
            taps=[np.exp(1j * 30 / 180 * np.pi)],
            noise_seed=243,
            block_tags=False)
        self.blocks_vector_source_x_0 = blocks.vector_source_b(testvec, True, 1, [])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_tagged_stream_align_0 = blocks.tagged_stream_align(gr.sizeof_char*1, 'frame_start')
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_char*1, frame_len)
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, [len(testvec), 4])
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(2, 8, "", False, gr.GR_LSB_FIRST)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 400))), True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.fadingui_netsink_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fadingui_ber_0, 0))
        self.connect((self.blocks_tagged_stream_align_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.channels_selective_fading_model_0, 0))
        self.connect((self.channels_selective_fading_model_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.channels_selective_fading_model_0, 0), (self.fadingui_netsink_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.digital_corr_est_cc_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.fadingui_netsink_1, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_tagged_stream_align_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.digital_corr_est_cc_0, 1), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.fadingui_phasecorrection_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_cma_equalizer_cc_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.fadingui_netsink_4, 0))
        self.connect((self.fadingui_phasecorrection_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.fadingui_phasecorrection_0, 0), (self.fadingui_netsink_3, 0))


    def get_testvec(self):
        return self.testvec

    def set_testvec(self, testvec):
        self.testvec = testvec
        self.set_frame_len(len(self.testvec) +4)
        self.blocks_vector_source_x_0.set_data(self.testvec, [])

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

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.channels_selective_fading_model_0.set_fDTs(((2*self.carrier_freq)/(3*10e8))/self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.rrc_taps)

    def get_qpsk_const(self):
        return self.qpsk_const

    def set_qpsk_const(self, qpsk_const):
        self.qpsk_const = qpsk_const

    def get_frame_len(self):
        return self.frame_len

    def set_frame_len(self, frame_len):
        self.frame_len = frame_len

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.channels_selective_fading_model_0.set_fDTs(((2*self.carrier_freq)/(3*10e8))/self.samp_rate)

    def get_access_code_symbols(self):
        return self.access_code_symbols

    def set_access_code_symbols(self, access_code_symbols):
        self.access_code_symbols = access_code_symbols
        self.digital_corr_est_cc_0.set_mark_delay(len(self.access_code_symbols) // 2)





def main(top_block_cls=qpsk_sim, options=None):
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

    tb.wait()


if __name__ == '__main__':
    main()
