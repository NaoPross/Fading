#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: AM_Simulation v2
# Author: sara
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time

from gnuradio import qtgui

class AM_Simulation(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "AM_Simulation v2")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("AM_Simulation v2")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "AM_Simulation")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1E6
        self.decim = decim = 16

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_1 = uhd.usrp_source(
            ",".join(("serial=309AF6A", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_1.set_clock_source('external', 0)
        self.uhd_usrp_source_1.set_center_freq(223e6, 0)
        self.uhd_usrp_source_1.set_rx_agc(False, 0)
        self.uhd_usrp_source_1.set_gain(1, 0)
        self.uhd_usrp_source_1.set_antenna('RX2', 0)
        self.uhd_usrp_source_1.set_bandwidth(200e3, 0)
        self.uhd_usrp_source_1.set_samp_rate(1e6)
        self.uhd_usrp_source_1.set_time_unknown_pps(uhd.time_spec())
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("serial=309AF59  ", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_clock_source('external', 0)
        self.uhd_usrp_sink_0.set_center_freq(223e6, 0)
        self.uhd_usrp_sink_0.set_gain(1, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(200e3, 0)
        self.uhd_usrp_sink_0.set_samp_rate(1e6)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec())
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "Orginal", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Orginal', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Demod', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, firdes.low_pass(1,samp_rate,samp_rate/(2*decim), 2000), 0, samp_rate)
        self.blocks_multiply_xx_0_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_xx_1 = blocks.add_vcc(1)
        self.band_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                500,
                60e3,
                4e3,
                firdes.WIN_HAMMING,
                6.76))
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 50E3, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_SQR_WAVE, 50e3, 1, 0, 0)
        self.analog_const_source_x_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 700e-3)
        self.analog_agc_xx_0 = analog.agc_cc(625e-6, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_1, 1))
        self.connect((self.band_pass_filter_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.blocks_multiply_xx_0_1, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.blocks_multiply_xx_0_1, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.freq_xlating_fir_filter_xxx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "AM_Simulation")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, 500, 60e3, 4e3, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.decim), 2000))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.decim), 2000))





def main(top_block_cls=AM_Simulation, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
