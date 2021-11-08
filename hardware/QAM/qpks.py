#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: QPSK Hardware Simultion
# Author: Pross Naoki, Halter Sara Cinzia
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
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget

from gnuradio import qtgui

class qpks(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "QPSK Hardware Simultion")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("QPSK Hardware Simultion")
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

        self.settings = Qt.QSettings("GNU Radio", "qpks")

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
        self.sps = sps = 4
        self.nfilts = nfilts = 32
        self.excess_bw = excess_bw = .35
        self.timing_loop_bw = timing_loop_bw = 2 * 3.141592653589793 / 100
        self.samp_rate = samp_rate = .4e6
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), excess_bw, 45*nfilts)
        self.qpsk_const = qpsk_const = digital.constellation_rect([0.707+0.707j, -0.707+0.707j, -0.707-0.707j, 0.707-0.707j], [0, 1, 3, 2],
        4, 2, 2, 1, 1).base()
        self.phase_bw = phase_bw = 2 * 3.141592653589793 / 100
        self.eq_ntaps = eq_ntaps = 15
        self.eq_mod = eq_mod = 2
        self.eq_gain = eq_gain = .01

        ##################################################
        # Blocks
        ##################################################
        self.params = Qt.QTabWidget()
        self.params_widget_0 = Qt.QWidget()
        self.params_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.params_widget_0)
        self.params_grid_layout_0 = Qt.QGridLayout()
        self.params_layout_0.addLayout(self.params_grid_layout_0)
        self.params.addTab(self.params_widget_0, 'Channel')
        self.params_widget_1 = Qt.QWidget()
        self.params_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.params_widget_1)
        self.params_grid_layout_1 = Qt.QGridLayout()
        self.params_layout_1.addLayout(self.params_grid_layout_1)
        self.params.addTab(self.params_widget_1, 'Receiver')
        self.top_grid_layout.addWidget(self.params)
        self.plots = Qt.QTabWidget()
        self.plots_widget_0 = Qt.QWidget()
        self.plots_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.plots_widget_0)
        self.plots_grid_layout_0 = Qt.QGridLayout()
        self.plots_layout_0.addLayout(self.plots_grid_layout_0)
        self.plots.addTab(self.plots_widget_0, 'Constellations')
        self.plots_widget_1 = Qt.QWidget()
        self.plots_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.plots_widget_1)
        self.plots_grid_layout_1 = Qt.QGridLayout()
        self.plots_layout_1.addLayout(self.plots_grid_layout_1)
        self.plots.addTab(self.plots_widget_1, 'Frequency')
        self.plots_widget_2 = Qt.QWidget()
        self.plots_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.plots_widget_2)
        self.plots_grid_layout_2 = Qt.QGridLayout()
        self.plots_layout_2.addLayout(self.plots_grid_layout_2)
        self.plots.addTab(self.plots_widget_2, 'Time')
        self.plots_widget_3 = Qt.QWidget()
        self.plots_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.plots_widget_3)
        self.plots_grid_layout_3 = Qt.QGridLayout()
        self.plots_layout_3.addLayout(self.plots_grid_layout_3)
        self.plots.addTab(self.plots_widget_3, 'Bits')
        self.top_grid_layout.addWidget(self.plots)
        self._phase_bw_range = Range(0, 1, .01, 2 * 3.141592653589793 / 100, 200)
        self._phase_bw_win = RangeWidget(self._phase_bw_range, self.set_phase_bw, 'Phase Bandwidth', "counter_slider", float)
        self.params_grid_layout_1.addWidget(self._phase_bw_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.params_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.params_grid_layout_1.setColumnStretch(c, 1)
        self._eq_gain_range = Range(0, .1, .001, .01, 200)
        self._eq_gain_win = RangeWidget(self._eq_gain_range, self.set_eq_gain, 'Equalizer Rate', "counter_slider", float)
        self.params_grid_layout_1.addWidget(self._eq_gain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.params_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.params_grid_layout_1.setColumnStretch(c, 1)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("serial=309AF6A  ", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_center_freq(2.4e9, 0)
        self.uhd_usrp_source_0.set_rx_agc(False, 0)
        self.uhd_usrp_source_0.set_normalized_gain(0.6, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
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
        self.uhd_usrp_sink_0.set_center_freq(2.4e9, 0)
        self.uhd_usrp_sink_0.set_normalized_gain(0.35, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec())
        self.qtgui_time_sink_x_2_0_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "Received (RX)", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_2_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_2_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2_0_0.enable_tags(False)
        self.qtgui_time_sink_x_2_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_2_0_0.enable_grid(False)
        self.qtgui_time_sink_x_2_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_2_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
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
                    self.qtgui_time_sink_x_2_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_2_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_2_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_2_0_0.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_2.addWidget(self._qtgui_time_sink_x_2_0_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.plots_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.plots_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "Modulated (TX)", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(False)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(True)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        self.qtgui_time_sink_x_2.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
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
                    self.qtgui_time_sink_x_2.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_2.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_2.addWidget(self._qtgui_time_sink_x_2_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.plots_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.plots_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1_0_1_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Locked", #name
            1
        )
        self.qtgui_freq_sink_x_1_0_1_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_1_0_1_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1_0_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1_0_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_1_0_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_1_0_1_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1_0_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1_0_1_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1_0_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1_0_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1_0_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_0_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_1_0_1_0.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_1.addWidget(self._qtgui_freq_sink_x_1_0_1_0_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.plots_grid_layout_1.setRowStretch(r, 1)
        for c in range(2, 3):
            self.plots_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1_0_1 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Equalized", #name
            1
        )
        self.qtgui_freq_sink_x_1_0_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1_0_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_1_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1_0_1.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1_0_1.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_1.addWidget(self._qtgui_freq_sink_x_1_0_1_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.plots_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.plots_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1_0_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Received", #name
            1
        )
        self.qtgui_freq_sink_x_1_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_1_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_1_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_1_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1_0_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_1_0_0.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_1.addWidget(self._qtgui_freq_sink_x_1_0_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.plots_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.plots_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Synchronized and filtered", #name
            1
        )
        self.qtgui_freq_sink_x_1_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_1_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_1_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_1.addWidget(self._qtgui_freq_sink_x_1_0_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.plots_grid_layout_1.setRowStretch(r, 1)
        for c in range(2, 3):
            self.plots_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Modulated (TX)", #name
            1
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_1.addWidget(self._qtgui_freq_sink_x_1_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.plots_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.plots_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_eye_sink_x_1 = qtgui.eye_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_eye_sink_x_1.set_update_time(0.10)
        self.qtgui_eye_sink_x_1.set_samp_per_symbol(sps)
        self.qtgui_eye_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_eye_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_eye_sink_x_1.enable_tags(True)
        self.qtgui_eye_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_eye_sink_x_1.enable_autoscale(False)
        self.qtgui_eye_sink_x_1.enable_grid(False)
        self.qtgui_eye_sink_x_1.enable_axis_labels(True)
        self.qtgui_eye_sink_x_1.enable_control_panel(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'blue', 'blue', 'blue', 'blue',
            'blue', 'blue', 'blue', 'blue', 'blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_eye_sink_x_1.set_line_label(i, "Eye [Re{{Data {0}}}]".format(round(i/2)))
                else:
                    self.qtgui_eye_sink_x_1.set_line_label(i, "Eye [Im{{Data {0}}}]".format(round((i-1)/2)))
            else:
                self.qtgui_eye_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_eye_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_eye_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_eye_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_eye_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_eye_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_eye_sink_x_1_win = sip.wrapinstance(self.qtgui_eye_sink_x_1.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_3.addWidget(self._qtgui_eye_sink_x_1_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.plots_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 1):
            self.plots_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_eye_sink_x_0 = qtgui.eye_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_eye_sink_x_0.set_update_time(0.10)
        self.qtgui_eye_sink_x_0.set_samp_per_symbol(sps)
        self.qtgui_eye_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_eye_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_eye_sink_x_0.enable_tags(True)
        self.qtgui_eye_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_eye_sink_x_0.enable_autoscale(False)
        self.qtgui_eye_sink_x_0.enable_grid(False)
        self.qtgui_eye_sink_x_0.enable_axis_labels(True)
        self.qtgui_eye_sink_x_0.enable_control_panel(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'blue', 'blue', 'blue', 'blue',
            'blue', 'blue', 'blue', 'blue', 'blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_eye_sink_x_0.set_line_label(i, "Eye [Re{{Data {0}}}]".format(round(i/2)))
                else:
                    self.qtgui_eye_sink_x_0.set_line_label(i, "Eye [Im{{Data {0}}}]".format(round((i-1)/2)))
            else:
                self.qtgui_eye_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_eye_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_eye_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_eye_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_eye_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_eye_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_eye_sink_x_0_win = sip.wrapinstance(self.qtgui_eye_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_eye_sink_x_0_win)
        self.qtgui_const_sink_x_2 = qtgui.const_sink_c(
            1024, #size
            "Locked", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_2.set_update_time(0.10)
        self.qtgui_const_sink_x_2.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_2.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_2.enable_autoscale(False)
        self.qtgui_const_sink_x_2.enable_grid(False)
        self.qtgui_const_sink_x_2.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_2_win = sip.wrapinstance(self.qtgui_const_sink_x_2.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_0.addWidget(self._qtgui_const_sink_x_2_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.plots_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.plots_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_1_0 = qtgui.const_sink_c(
            1024, #size
            "Equalized", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_1_0.set_update_time(0.10)
        self.qtgui_const_sink_x_1_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_1_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_1_0.enable_autoscale(False)
        self.qtgui_const_sink_x_1_0.enable_grid(False)
        self.qtgui_const_sink_x_1_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_1_0_win = sip.wrapinstance(self.qtgui_const_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_0.addWidget(self._qtgui_const_sink_x_1_0_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.plots_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.plots_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0_0 = qtgui.const_sink_c(
            2048, #size
            "Received", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0_0_0.enable_grid(False)
        self.qtgui_const_sink_x_0_0_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_0.addWidget(self._qtgui_const_sink_x_0_0_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.plots_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.plots_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            2048, #size
            "Synchronized and filtered", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0_0.enable_grid(False)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_0.addWidget(self._qtgui_const_sink_x_0_0_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.plots_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.plots_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "Sent (with ISI)", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_0.addWidget(self._qtgui_const_sink_x_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.plots_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.plots_grid_layout_0.setColumnStretch(c, 1)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, timing_loop_bw, rrc_taps, nfilts, nfilts/2, 1.5, int(sps / 2))
        self.digital_map_bb_0 = digital.map_bb([0, 1, 3, 2])
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(4)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(phase_bw, 4, False)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=qpsk_const,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=excess_bw,
            verbose=False,
            log=False)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(qpsk_const)
        self.digital_cma_equalizer_cc_0 = digital.cma_equalizer_cc(eq_ntaps, eq_mod, eq_gain, int(sps / 2))
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/god/Documents/Fading/hardware/QPSK/lena512color.tiff', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.qtgui_const_sink_x_1_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.qtgui_freq_sink_x_1_0_1, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_2, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_eye_sink_x_1, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_freq_sink_x_1_0_1_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_time_sink_x_2_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_cma_equalizer_cc_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.qtgui_freq_sink_x_1_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_const_sink_x_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_1_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "qpks")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 45*self.nfilts))
        self.qtgui_eye_sink_x_0.set_samp_per_symbol(self.sps)
        self.qtgui_eye_sink_x_1.set_samp_per_symbol(self.sps)

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

    def get_timing_loop_bw(self):
        return self.timing_loop_bw

    def set_timing_loop_bw(self, timing_loop_bw):
        self.timing_loop_bw = timing_loop_bw
        self.digital_pfb_clock_sync_xxx_0.set_loop_bandwidth(self.timing_loop_bw)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_eye_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_eye_sink_x_1.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_1_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_1_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_1_0_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_1_0_1_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_2_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.rrc_taps)

    def get_qpsk_const(self):
        return self.qpsk_const

    def set_qpsk_const(self, qpsk_const):
        self.qpsk_const = qpsk_const

    def get_phase_bw(self):
        return self.phase_bw

    def set_phase_bw(self, phase_bw):
        self.phase_bw = phase_bw
        self.digital_costas_loop_cc_0.set_loop_bandwidth(self.phase_bw)

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





def main(top_block_cls=qpks, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")

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
