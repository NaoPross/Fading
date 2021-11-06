#!/usr/bin/env python3

from dearpygui.dearpygui import *
from dearpygui.demo import show_demo

import qpks

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

with window(label="RX DSP Flow Graph", width=800, height=800, on_close=_on_params_close, pos=(100,100), tag="rx_win"):
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
            with node_attribute(attribute_type=mvNode_Attr_Static):
                add_input_float(label="Gain", width=150)

            with node_attribute(tag="eq_in", attribute_type=mvNode_Attr_Input):
                add_text("Input")

            with node_attribute(tag="eq_out", attribute_type=mvNode_Attr_Output):
                add_text("Equalized")

        with node(label="Phase Locked Loop", pos=(600, 200)):
            with node_attribute(tag="pll_in", attribute_type=mvNode_Attr_Input):
                add_text("Input")

            with node_attribute(tag="pll_out", attribute_type=mvNode_Attr_Output):
                add_text("Locked")


        add_node_link(get_alias_id("src_out"), get_alias_id("clksync_in"))
        add_node_link(get_alias_id("clksync_out"), get_alias_id("eq_in"))
        add_node_link(get_alias_id("eq_out"), get_alias_id("pll_in"))


<<<<<<< HEAD
with window(label="Example Window"):
    add_text("Hello world")
=======
#================================================
# Start window and main loop
>>>>>>> origin/master

show_viewport()
start_dearpygui()
destroy_context()
