#!/usr/bin/env python3

# Python stdlib
import sys

# Grahical libraries
from dearpygui.dearpygui import *
import dearpygui._dearpygui as internal_dpg
from dearpygui.demo import show_demo

# Detect (unix) signals
import signal

# Mathematics
import numpy as np

# For debugging
import logging

# Remote resources
import net

#================================================
# Debugging tools

logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

#================================================
# Initialize DearPyGUI

create_context()
create_viewport(title="Fading Demonstrator")
setup_dearpygui()

# Show demo for dev
show_demo()


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
# Settings Window

with window(label="Settings", width=200, height=400, pos=(25, 450), tag="sim_win"):
    with child_window(autosize_x=True, height=100):
        add_button(label="Toggle Fullscreen", callback= toggle_viewport_fullscreen)

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
# Network plots Window

recv_plot = net.network_plot(url="udp://localhost:31415", dtype=float, nsamples=100, \
        label="Test", height=300, width=800)

plots = {
    recv_plot: "plt_ampl"
}

with window(label="Time domain plots", width=800, height=400, pos=(850,25)):
    with recv_plot:
        add_plot_axis(mvXAxis, label="Time")
        add_plot_axis(mvYAxis, label="Amplitude", tag="axis")

        add_line_series(recv_plot.xdata, recv_plot.ydata, parent="axis", tag="plt_ampl")

#================================================
# Start GUI and main loop

# Start window and main loop
show_viewport()

# Main loop
while is_dearpygui_running():
    for plt, tag in plots.items():
        plt.refresh_series(tag)

    render_dearpygui_frame()

#================================================
# Close everything

# clean up gui
destroy_context()
