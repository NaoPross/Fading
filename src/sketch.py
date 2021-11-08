#!/usr/bin/env python3

from dearpygui.dearpygui import *
from dearpygui.demo import show_demo

import qpks as qp

from math import sin #für test Sijnal 

# Create GL context and initialize DearPyGUI
create_context()
create_viewport()
setup_dearpygui()

# Show demo for dev
show_demo()


#================================================
# GUI Callback functions

def _on_params_close():
    pass

def _on_rx_node_link(sender, app_data):
    link_id_1, link_id_2 = app_data
    print(app_data)
    add_node_link(link_id_1, link_id_2, parent=sender)

def _on_rx_node_delink(sender, app_data):
    link_id = app_data
    delete_item(link_id)

#================================================
# Flow Graph Window

# with window(label="RX DSP Flow Graph", width=800, height=800, on_close=_on_params_close, pos=(100,100), tag="rx_win"):
#     with node_editor(callback=_on_rx_node_link, delink_callback=_on_rx_node_delink):
#         with node(label="USRP Source", pos=(20,100)):
#             with node_attribute(tag="src_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Signal from antenna")

#         with node(label="Clock Sync", pos=(200,200)):
#             with node_attribute(tag="clksync_in", attribute_type=mvNode_Attr_Input):
#                 add_text("Input")

#             with node_attribute(tag="clksync_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Synchronized")

#         with node(label="Equalizer", pos=(350,100)):
#             with node_attribute(attribute_type=mvNode_Attr_Static):
#                 add_input_float(label="Gain", width=150)

#             with node_attribute(tag="eq_in", attribute_type=mvNode_Attr_Input):
#                 add_text("Input")

#             with node_attribute(tag="eq_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Equalized")

#         with node(label="Phase Locked Loop", pos=(600, 200)):
#             with node_attribute(tag="pll_in", attribute_type=mvNode_Attr_Input):
#                 add_text("Input")

#             with node_attribute(tag="pll_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Locked")


#         add_node_link(get_alias_id("src_out"), get_alias_id("clksync_in"))
#         add_node_link(get_alias_id("clksync_out"), get_alias_id("eq_in"))
#         add_node_link(get_alias_id("eq_out"), get_alias_id("pll_in"))


#================================================
# QPSK Window

q = qp.qpsk_nogui() # Klasse initalisieren !!!

with window(label="QPSK", width=1500, height=800, on_close=_on_params_close, pos=(100,100), tag="rx_win"):
    with node_editor(callback=_on_rx_node_link, delink_callback=_on_rx_node_delink):
        
        with node(label="USRP Source ", pos=(20,100)):
            with node_attribute(tag="src_out", attribute_type=mvNode_Attr_Output):
                add_text("Signal Source Random")
                print(q.analog_random_source_x_0)
                # TO DO: Signal Plot

        with node(label="Constellation Modulator", pos=(200,200)):
            with node_attribute(tag="modul_in", attribute_type=mvNode_Attr_Input):
                add_text("Input")
                add_text(f'Sample {q.sps}')

            with node_attribute(tag="modul_out", attribute_type=mvNode_Attr_Output):
                add_text("Output")

        with node(label="Channel Model", pos=(420,100)):
            with node_attribute(tag="channel_in", attribute_type=mvNode_Attr_Input):
                add_text("Input")

            with node_attribute(tag="channel_out", attribute_type=mvNode_Attr_Output):
                add_text("Output")

        with node(label="Clock Sync", pos=(550,200)):
            with node_attribute(tag="clksync_in", attribute_type=mvNode_Attr_Input):
                add_text("Input")

            with node_attribute(tag="clksync_out", attribute_type=mvNode_Attr_Output):
                add_text("Synchronized")


        with node(label="Equalizer", pos=(700,100)):
            with node_attribute(attribute_type=mvNode_Attr_Static):
                add_input_float(label="Gain", width=150)

            with node_attribute(tag="eq_in", attribute_type=mvNode_Attr_Input):
                add_text("Input")

            with node_attribute(tag="eq_out", attribute_type=mvNode_Attr_Output):
                add_text("Equalized")


        with node(label="Phase Locked Loop", pos=(950, 200)):
            with node_attribute(tag="pll_in", attribute_type=mvNode_Attr_Input):
                add_text("Input")

            with node_attribute(tag="pll_out", attribute_type=mvNode_Attr_Output):
                add_text("Locked")


        add_node_link(get_alias_id("src_out"), get_alias_id("modul_in"))
        add_node_link(get_alias_id("modul_out"), get_alias_id("channel_in"))
        add_node_link(get_alias_id("channel_out"), get_alias_id("clksync_in"))
        add_node_link(get_alias_id("clksync_out"), get_alias_id("eq_in"))
        add_node_link(get_alias_id("eq_out"), get_alias_id("pll_in"))



#================================================
# Plot Time Window Test

# creating data
sindatax = []
sindatay = []
for i in range(0, 500):
    sindatax.append(i / 1000)
    sindatay.append(0.5 + 0.5 * sin(50 * i / 1000))

with window(label="Plots"):
    add_text("Hello world")
    # create plot
    with plot(label="Line Series", height=400, width=400):
        # optionally create legend
        add_plot_legend()

        # REQUIRED: create x and y axes
        add_plot_axis(mvXAxis, label="x")
        add_plot_axis(mvYAxis, label="y", tag="y_axis")

        # series belong to a y axis
        add_line_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)", parent="y_axis")
#================================================



# Start window and main loop


show_viewport()
start_dearpygui()
destroy_context()
