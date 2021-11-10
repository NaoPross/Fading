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


# Create GL context and initialize DearPyGUI
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

    def construct_gui(self, width, height):
        # Create plot
        with plot(label=self.title, height=height, width=width):
             add_plot_legend()
             add_plot_axis(mvXAxis, label=self.xlabel)
             add_plot_axis(mvYAxis, label=self.ylabel)

    def work(self, input_items, output_items):
        # This is a sink (no output)
        return 0


class pygui_constellation_block(gr.sync_block):
    def __init__(self, title="Constellation", xlabel="In-Phase", ylabel="Quadrature"):
        gr.sync_block.__init__(self, name="PyGUI Constellation Diagram",    
                in_sig=[np.complex64], out_sig=None)

        self.title = title
        self.xlabel = xlabel
        selt.ylabel = ylabel


#================================================
# GUI Callback functions

def _on_flowgraph_close():
    pass

def _on_rx_node_link(sender, app_data):
    link_id_1, link_id_2 = app_data
    print(app_data)
    add_node_link(link_id_1, link_id_2, parent=sender)

def _on_rx_node_delink(sender, app_data):
    link_id = app_data
    delete_item(link_id)

#================================================
# Set up GNURadio simulation

sim = qpsk.qpsk_nogui()

# Catch signals
def sim_sig_handler(sig=None, frame=None):
    sim.stop()
    sim.wait()
    sys.exit(0)

# TODO: create GUI handlers
signal.signal(signal.SIGINT, sim_sig_handler)
signal.signal(signal.SIGTERM, sim_sig_handler);

# Add GUI blocks
locked_time_plot = pygui_plot_block(title="Locked signal", xlabel="t")
sim.connect((sim.digital_costas_loop_cc_0, 0), (locked_time_plot, 0))

#================================================
# Simulation Control Window

with window(label="Simulation", width=200, height=400, pos=(25, 450), tag="sim_win"):
    add_text("Simulation state:")

    with group(horizontal=True):
        def on_sim_start_btn_clicked():
            sim.start()

            configure_item("sim_start_btn", enabled=False)
            configure_item("sim_stop_btn", enabled=True)

        def on_sim_stop_btn_clicked():
            sim.stop()
            sim.wait()

            configure_item("sim_start_btn", enabled=True)
            configure_item("sim_stop_btn", enabled=False)

        add_button(label="Start", tag="sim_start_btn", callback=on_sim_start_btn_clicked)
        add_button(label="Stop", enabled=False, tag="sim_stop_btn", callback=on_sim_stop_btn_clicked)

#================================================
# Flow Graph Window

with window(label="RX DSP Flow Graph", width=800, height=400, on_close=_on_flowgraph_close, pos=(25,25), tag="rx_win"):
    with node_editor(callback=_on_rx_node_link, delink_callback=_on_rx_node_delink):
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

            with node_attribute(tag="eq_out", attribute_type=mvNode_Attr_Output):
                add_text("Equalized")

            with node_attribute(attribute_type=mvNode_Attr_Static):
                add_knob_float(label="Gain")

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
# QPSK Window

# q = qp.qpsk_nogui()

# with window(label="QPSK", width=1500, height=800, on_close=_on_flowgraph_close, pos=(100,100), tag="rx_win"):
#     with node_editor(callback=_on_rx_node_link, delink_callback=_on_rx_node_delink):
#         
#         with node(label="USRP Source ", pos=(20,100)):
#             with node_attribute(tag="src_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Signal Source Random")
#                 print(q.analog_random_source_x_0)
#                 # TO DO: Signal Plot
# 
#         with node(label="Constellation Modulator", pos=(200,200)):
#             with node_attribute(tag="modul_in", attribute_type=mvNode_Attr_Input):
#                 add_text("Input")
#                 add_text(f'Sample {q.sps}')
# 
#             with node_attribute(tag="modul_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Output")
# 
#         with node(label="Channel Model", pos=(420,100)):
#             with node_attribute(tag="channel_in", attribute_type=mvNode_Attr_Input):
#                 add_text("Input")
# 
#             with node_attribute(tag="channel_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Output")
# 
#         with node(label="Clock Sync", pos=(550,200)):
#             with node_attribute(tag="clksync_in", attribute_type=mvNode_Attr_Input):
#                 add_text("Input")
# 
#             with node_attribute(tag="clksync_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Synchronized")
# 
# 
#         with node(label="Equalizer", pos=(700,100)):
#             with node_attribute(attribute_type=mvNode_Attr_Static):
#                 add_input_float(label="Gain", width=150)
# 
#             with node_attribute(tag="eq_in", attribute_type=mvNode_Attr_Input):
#                 add_text("Input")
# 
#             with node_attribute(tag="eq_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Equalized")
# 
# 
#         with node(label="Phase Locked Loop", pos=(950, 200)):
#             with node_attribute(tag="pll_in", attribute_type=mvNode_Attr_Input):
#                 add_text("Input")
# 
#             with node_attribute(tag="pll_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Locked")
# 
# 
#         add_node_link(get_alias_id("src_out"), get_alias_id("modul_in"))
#         add_node_link(get_alias_id("modul_out"), get_alias_id("channel_in"))
#         add_node_link(get_alias_id("channel_out"), get_alias_id("clksync_in"))
#         add_node_link(get_alias_id("clksync_out"), get_alias_id("eq_in"))
#         add_node_link(get_alias_id("eq_out"), get_alias_id("pll_in"))
# 


#================================================
# Plot Time Window Test

# creating data
# sindatax = []
# sindatay = []
# for i in range(0, 500):
#     sindatax.append(i / 1000)
#     sindatay.append(0.5 + 0.5 * sin(50 * i / 1000))
# 
# with window(label="Plots"):
#     add_text("Hello world")
#     # create plot
#     with plot(label="Line Series", height=400, width=400):
#         # optionally create legend
#         add_plot_legend()
# 
#         # REQUIRED: create x and y axes
#         add_plot_axis(mvXAxis, label="x")
#         add_plot_axis(mvYAxis, label="y", tag="y_axis")
# 
#         # series belong to a y axis
#         add_line_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)", parent="y_axis")

#================================================



# Start window and main loop
show_viewport()
start_dearpygui()

# clean up gui
destroy_context()

# Stop GNURadio
sim.stop()
sim.wait()
