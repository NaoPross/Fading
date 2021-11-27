#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: QAM mit Fading
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
import numpy
from gnuradio import channels
from gnuradio import digital
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import fadingui
import numpy as np

from gnuradio import qtgui

class qam_fading_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "QAM mit Fading")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("QAM mit Fading")
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

        self.settings = Qt.QSettings("GNU Radio", "qam_fading_block")

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
        self.excess_bw = excess_bw = 350e-3
        self.timing_loop_bw = timing_loop_bw = 2 * 3.141592653589793 / 100
        self.time_offset = time_offset = 1.0
        self.samp_rate = samp_rate = 32000
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), excess_bw, 45*nfilts)
        self.phase_bw = phase_bw = 2 * 3.141592653589793 / 100
        self.noise_volt = noise_volt = 0.0001
        self.freq_offset = freq_offset = 0
        self.fading_1 = fading_1 = 2
        self.eq_ntaps = eq_ntaps = 15
        self.eq_mod = eq_mod = 1
        self.eq_gain = eq_gain = .01
        self.const = const = digital.constellation_16qam().base()
        self.chn_taps = chn_taps = [1.0 + 0.0j, ]
        self.amp_1 = amp_1 = 0.2
        self.LOS_NLOS = LOS_NLOS = 1

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
        self.params_widget_2 = Qt.QWidget()
        self.params_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.params_widget_2)
        self.params_grid_layout_2 = Qt.QGridLayout()
        self.params_layout_2.addLayout(self.params_grid_layout_2)
        self.params.addTab(self.params_widget_2, 'Fading')
        self.top_grid_layout.addWidget(self.params)
        self._timing_loop_bw_range = Range(0, 200e-3, 10e-3, 2 * 3.141592653589793 / 100, 200)
        self._timing_loop_bw_win = RangeWidget(self._timing_loop_bw_range, self.set_timing_loop_bw, 'Time Bandwidth', "counter_slider", float)
        self.params_grid_layout_0.addWidget(self._timing_loop_bw_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.params_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.params_grid_layout_0.setColumnStretch(c, 1)
        self._time_offset_range = Range(0.999, 1.001, 0.0001, 1.0, 200)
        self._time_offset_win = RangeWidget(self._time_offset_range, self.set_time_offset, 'Timing Offset', "counter_slider", float)
        self.params_grid_layout_0.addWidget(self._time_offset_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.params_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.params_grid_layout_0.setColumnStretch(c, 1)
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
        self.top_grid_layout.addWidget(self.plots)
        self._phase_bw_range = Range(0, 1, .01, 2 * 3.141592653589793 / 100, 200)
        self._phase_bw_win = RangeWidget(self._phase_bw_range, self.set_phase_bw, 'Phase Bandwidth', "counter_slider", float)
        self.params_grid_layout_1.addWidget(self._phase_bw_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.params_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.params_grid_layout_1.setColumnStretch(c, 1)
        self._noise_volt_range = Range(0, 1, 0.01, 0.0001, 200)
        self._noise_volt_win = RangeWidget(self._noise_volt_range, self.set_noise_volt, 'Noise Voltage', "counter_slider", float)
        self.params_grid_layout_0.addWidget(self._noise_volt_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.params_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.params_grid_layout_0.setColumnStretch(c, 1)
        self._freq_offset_range = Range(-100e-3, 100e-3, 1e-3, 0, 200)
        self._freq_offset_win = RangeWidget(self._freq_offset_range, self.set_freq_offset, 'Frequency Offset', "counter_slider", float)
        self.params_grid_layout_0.addWidget(self._freq_offset_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.params_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.params_grid_layout_0.setColumnStretch(c, 1)
        self._eq_gain_range = Range(0, .1, .001, .01, 200)
        self._eq_gain_win = RangeWidget(self._eq_gain_range, self.set_eq_gain, 'Equalizer Rate', "counter_slider", float)
        self.params_grid_layout_1.addWidget(self._eq_gain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.params_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.params_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Decoded", #name
            3 #number of inputs
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


        labels = ['Received', 'Sent', 'Signal 3', 'Signal 4', 'Signal 5',
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


        for i in range(3):
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
        self.plots_grid_layout_2.addWidget(self._qtgui_time_sink_x_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.plots_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.plots_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_2_1 = qtgui.freq_sink_f(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            2
        )
        self.qtgui_freq_sink_x_2_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_2_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_2_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_2_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_2_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_2_1.enable_grid(False)
        self.qtgui_freq_sink_x_2_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_2_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_2_1.enable_control_panel(False)


        self.qtgui_freq_sink_x_2_1.set_plot_pos_half(not True)

        labels = ['Fading', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_2_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_2_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_2_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_2_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_2_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_2_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_2_1.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_1.addWidget(self._qtgui_freq_sink_x_2_1_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.plots_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.plots_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Channel", #name
            2
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['Fading', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.plots_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.plots_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_2 = qtgui.const_sink_c(
            1024, #size
            "Locked", #name
            2 #number of inputs
        )
        self.qtgui_const_sink_x_2.set_update_time(0.10)
        self.qtgui_const_sink_x_2.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_2.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_2.enable_autoscale(False)
        self.qtgui_const_sink_x_2.enable_grid(False)
        self.qtgui_const_sink_x_2.enable_axis_labels(True)


        labels = ['fading', 'normal', '', '', '',
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

        for i in range(2):
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
        self.plots_grid_layout_0.addWidget(self._qtgui_const_sink_x_2_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.plots_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.plots_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_1 = qtgui.const_sink_c(
            1024, #size
            "Equalized", #name
            2 #number of inputs
        )
        self.qtgui_const_sink_x_1.set_update_time(0.10)
        self.qtgui_const_sink_x_1.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_1.enable_autoscale(False)
        self.qtgui_const_sink_x_1.enable_grid(False)
        self.qtgui_const_sink_x_1.enable_axis_labels(True)


        labels = ['fading', 'normal', '', '', '',
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

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_1_win = sip.wrapinstance(self.qtgui_const_sink_x_1.pyqwidget(), Qt.QWidget)
        self.plots_grid_layout_0.addWidget(self._qtgui_const_sink_x_1_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.plots_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.plots_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            2048, #size
            "Synchronized", #name
            2 #number of inputs
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(False)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


        labels = ['fading', 'normal', '', '', '',
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

        for i in range(2):
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
        self.plots_grid_layout_0.addWidget(self._qtgui_const_sink_x_0_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.plots_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.plots_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            2048, #size
            "Channel", #name
            2 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['fading', 'normal', '', '', '',
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

        for i in range(2):
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
        self.fadingui_multipath_fading_0 = fadingui.multipath_fading(amplitudes=[0.2,0.2], delays=[sps+1,sps+1])
        self._fading_1_range = Range(1, 30, 1, 2, 200)
        self._fading_1_win = RangeWidget(self._fading_1_range, self.set_fading_1, 'Fading', "counter_slider", int)
        self.params_grid_layout_2.addWidget(self._fading_1_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.params_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.params_grid_layout_2.setColumnStretch(c, 1)
        self.digital_pfb_clock_sync_xxx_0_0 = digital.pfb_clock_sync_ccf(sps , timing_loop_bw, rrc_taps, nfilts, nfilts/2, 1.5, 1)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, timing_loop_bw, rrc_taps, nfilts, nfilts/2, 1.5, 1)
        self.digital_map_bb_0_0 = digital.map_bb([0, 1, 3, 2])
        self.digital_map_bb_0 = digital.map_bb([0, 1, 3, 2])
        self.digital_diff_decoder_bb_0_0 = digital.diff_decoder_bb(4)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(4)
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc(phase_bw, 4, False)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(phase_bw, 4, False)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=const,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=excess_bw,
            verbose=False,
            log=False)
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(const)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(const)
        self.digital_cma_equalizer_cc_0_0 = digital.cma_equalizer_cc(eq_ntaps, eq_mod, eq_gain, 2)
        self.digital_cma_equalizer_cc_0 = digital.cma_equalizer_cc(eq_ntaps, eq_mod, eq_gain, 2)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise_volt,
            frequency_offset=freq_offset,
            epsilon=time_offset,
            taps=chn_taps,
            noise_seed=0,
            block_tags=False)
        self.blocks_unpack_k_bits_bb_0_1 = blocks.unpack_k_bits_bb(2)
        self.blocks_unpack_k_bits_bb_0_0 = blocks.unpack_k_bits_bb(2)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(2)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, 50)
        self.blocks_char_to_float_0_1 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 1000))), True)
        self._amp_1_range = Range(0, 5, 0.1, 0.2, 200)
        self._amp_1_win = RangeWidget(self._amp_1_range, self.set_amp_1, 'Ampliude', "counter_slider", float)
        self.params_grid_layout_2.addWidget(self._amp_1_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.params_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.params_grid_layout_2.setColumnStretch(c, 1)
        self._LOS_NLOS_range = Range(0, 1, 1, 1, 200)
        self._LOS_NLOS_win = RangeWidget(self._LOS_NLOS_range, self.set_LOS_NLOS, 'LOS_NLOS', "counter_slider", int)
        self.params_grid_layout_2.addWidget(self._LOS_NLOS_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.params_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.params_grid_layout_2.setColumnStretch(c, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_unpack_k_bits_bb_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_freq_sink_x_2_1, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_char_to_float_0_1, 0), (self.qtgui_freq_sink_x_2_1, 1))
        self.connect((self.blocks_char_to_float_0_1, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.blocks_delay_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0_0, 0), (self.blocks_char_to_float_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0_1, 0), (self.blocks_char_to_float_0_1, 0))
        self.connect((self.channels_channel_model_0, 0), (self.digital_pfb_clock_sync_xxx_0_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.fadingui_multipath_fading_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_const_sink_x_0, 1))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.qtgui_const_sink_x_1, 0))
        self.connect((self.digital_cma_equalizer_cc_0_0, 0), (self.digital_costas_loop_cc_0_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0_0, 0), (self.qtgui_const_sink_x_1, 1))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.digital_diff_decoder_bb_0_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_2, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.digital_constellation_decoder_cb_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.qtgui_const_sink_x_2, 1))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_0, 0), (self.digital_map_bb_0_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.digital_map_bb_0_0, 0), (self.blocks_unpack_k_bits_bb_0_1, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_cma_equalizer_cc_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0_0, 0), (self.digital_cma_equalizer_cc_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0_0, 0), (self.qtgui_const_sink_x_0_0, 1))
        self.connect((self.fadingui_multipath_fading_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.fadingui_multipath_fading_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.fadingui_multipath_fading_0, 0), (self.qtgui_freq_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "qam_fading_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

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

    def get_timing_loop_bw(self):
        return self.timing_loop_bw

    def set_timing_loop_bw(self, timing_loop_bw):
        self.timing_loop_bw = timing_loop_bw
        self.digital_pfb_clock_sync_xxx_0.set_loop_bandwidth(self.timing_loop_bw)
        self.digital_pfb_clock_sync_xxx_0_0.set_loop_bandwidth(self.timing_loop_bw)

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
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_2_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.rrc_taps)
        self.digital_pfb_clock_sync_xxx_0_0.update_taps(self.rrc_taps)

    def get_phase_bw(self):
        return self.phase_bw

    def set_phase_bw(self, phase_bw):
        self.phase_bw = phase_bw
        self.digital_costas_loop_cc_0.set_loop_bandwidth(self.phase_bw)
        self.digital_costas_loop_cc_0_0.set_loop_bandwidth(self.phase_bw)

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

    def get_fading_1(self):
        return self.fading_1

    def set_fading_1(self, fading_1):
        self.fading_1 = fading_1

    def get_eq_ntaps(self):
        return self.eq_ntaps

    def set_eq_ntaps(self, eq_ntaps):
        self.eq_ntaps = eq_ntaps

    def get_eq_mod(self):
        return self.eq_mod

    def set_eq_mod(self, eq_mod):
        self.eq_mod = eq_mod
        self.digital_cma_equalizer_cc_0.set_modulus(self.eq_mod)
        self.digital_cma_equalizer_cc_0_0.set_modulus(self.eq_mod)

    def get_eq_gain(self):
        return self.eq_gain

    def set_eq_gain(self, eq_gain):
        self.eq_gain = eq_gain
        self.digital_cma_equalizer_cc_0.set_gain(self.eq_gain)
        self.digital_cma_equalizer_cc_0_0.set_gain(self.eq_gain)

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def get_chn_taps(self):
        return self.chn_taps

    def set_chn_taps(self, chn_taps):
        self.chn_taps = chn_taps
        self.channels_channel_model_0.set_taps(self.chn_taps)

    def get_amp_1(self):
        return self.amp_1

    def set_amp_1(self, amp_1):
        self.amp_1 = amp_1

    def get_LOS_NLOS(self):
        return self.LOS_NLOS

    def set_LOS_NLOS(self, LOS_NLOS):
        self.LOS_NLOS = LOS_NLOS





def main(top_block_cls=qam_fading_block, options=None):
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
