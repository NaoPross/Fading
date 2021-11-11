#!/usr/bin/env python3

# Python stdlib
import sys

# Grahical libraries
from dearpygui.dearpygui import *
from dearpygui.demo import show_demo

# Detect (unix) signals
import signal

# GNURadio tools
from gnuradio import gr

# Mathematics
import numpy as np

# Our interface for simulation / hardware
import qpsk

# For debugging
import logging

#================================================
# Debugging tools

logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

#================================================
# Initialize DearPyGUI

create_context()
create_viewport()
setup_dearpygui()

# Show demo for dev
show_demo()

#================================================
# Custom GNURadio blocks

class pygui_plot_block(gr.sync_block):
    def __init__(self, title="Plot", xlabel="x", ylabel="y"):
        gr.sync_block.__init__(self, name="PyGUI Plot",
                in_sig=[np.complex64], out_sig=None)

        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

        # TODO: parametrize with nsamples
        self.buffer = np.linspace(0, 1, 1000)

    def construct_gui(self, width, height, **kwargs):
        # Create plot
        with plot(label=self.title, height=height, width=width, **kwargs):
             add_plot_legend()
             add_plot_axis(mvXAxis, label=self.xlabel)
             add_plot_axis(mvYAxis, label=self.ylabel)

    def work(self, input_items, output_items):
        # This is a sink (no output)
        # TODO: add samples to display buffer
        return 0


class pygui_constellation_block(gr.sync_block):
    def __init__(self, title="Constellation", xlabel="In-Phase", ylabel="Quadrature"):
        gr.sync_block.__init__(self, name="PyGUI Constellation Diagram",    
                in_sig=[np.complex64], out_sig=None)

        self.title = title
        self.xlabel = xlabel
        selt.ylabel = ylabel

    def construct_gui(self, width, height, **kwargs):
        # TODO: Create a widget based ons scatter plot
        pass

    def work(self, input_items, output_items):
        # This is a sink (no output)
        # TODO: add samples to display buffer
        return 0


#================================================
# GUI Callback functions

# Flow graph window
def on_rx_node_link(sender, app_data):
    link_id_1, link_id_2 = app_data
    add_node_link(link_id_1, link_id_2, parent=sender)

def on_rx_node_delink(sender, app_data):
    link_id = app_data
    delete_item(link_id)

#================================================
# Set up GNURadio simulation

# Global variables, yes I know they are ugly
sim = qpsk.qpsk_nogui()
sim_running = False

# Catch signals
def sim_sig_handler(sig=None, frame=None):
    sim.stop()
    sim.wait()
    sys.exit(0)

# TODO: create GUI handlers
signal.signal(signal.SIGINT, sim_sig_handler)
signal.signal(signal.SIGTERM, sim_sig_handler);

# Add GUI blocks
locked_time_plot = pygui_plot_block(title="Locked signal", ylabel="Amplitude", xlabel="Time")
sim.connect((sim.digital_costas_loop_cc_0, 0), (locked_time_plot, 0))

#================================================
# Settings Window

with window(label="Settings", width=200, height=400, pos=(25, 450), tag="sim_win"):
    with child_window(autosize_x=True, height=100):
        add_button(label="Toggle Fullscreen", callback= toggle_viewport_fullscreen)

    with child_window(autosize_x=True):
        with group(horizontal=True):
            add_text("Simulation running:")
            add_text("false", tag="sim_running_lbl")

        with group(tag="sim_grp", horizontal=True):
            def on_sim_start_btn_clicked():
                global sim_running

                if sim_running:
                    logger.error("Simulation is already running")
                    return

                sim.start()
                sim_running = True
                logger.debug("Started simulation")

            def on_sim_stop_btn_clicked():
                global sim_running

                if not sim_running:
                    logger.error("Simulation not running")
                    return

                sim.stop()
                sim.wait()
                sim_running = False
                logger.debug("Stopped simulation")

            add_button(label="Start", tag="sim_start_btn", callback=on_sim_start_btn_clicked)
            add_button(label="Stop", tag="sim_stop_btn", callback=on_sim_stop_btn_clicked)

#================================================
# Flow Graph Window

with window(label="RX DSP Flow Graph", width=800, height=400, pos=(25,25), tag="rx_win"):
    with node_editor(callback=on_rx_node_link, delink_callback=on_rx_node_delink):
        with node(label="USRP Source", pos=(20,100)):
            with node_attribute(tag="src_out", attribute_type=mvNode_Attr_Output):
                add_text("Signal from antenna")

        with node(label="Clock Sync", pos=(200,200)):
            with node_attribute(tag="clksync_in", attribute_type=mvNode_Attr_Input):
                add_text("Input")

            with node_attribute(tag="clksync_out", attribute_type=mvNode_Attr_Output):
                add_text("Synchronized")

        with node(label="Equalizer", pos=(350,100)):
            with node_attribute(tag="eq_in", attribute_type=mvNode_Attr_Input):
                add_text("Input")

            with node_attribute(attribute_type=mvNode_Attr_Static):
                add_knob_float(label="Gain")

            with node_attribute(tag="eq_out", attribute_type=mvNode_Attr_Output):
                add_text("Equalized")

        with node(label="Phase Locked Loop", pos=(600, 200)):
            with node_attribute(tag="pll_in", attribute_type=mvNode_Attr_Input):
                add_text("Input")

            with node_attribute(tag="pll_out", attribute_type=mvNode_Attr_Output):
                add_text("Locked")
                add_knob_float(label="Loop BW")


        add_node_link(get_alias_id("src_out"), get_alias_id("clksync_in"))
        add_node_link(get_alias_id("clksync_out"), get_alias_id("eq_in"))
        add_node_link(get_alias_id("eq_out"), get_alias_id("pll_in"))

#================================================
# Time plots Window

with window(label="Time domain plots", width=800, height=400, pos=(850,25), tag="time_plots_win"):
    locked_time_plot.construct_gui(width=780, height=300)

#================================================
# Start GUI

# Start window and main loop
show_viewport()
start_dearpygui()

# clean up gui
destroy_context()
