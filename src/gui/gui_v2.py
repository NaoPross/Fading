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
create_viewport(title="Fading Demonstrator",width=1200, height=800)
setup_dearpygui()

# Show demo for dev
show_demo()



#================================================
# GUI Callback functions

# Menu Bar 
def exit(sender, data):
    stop_dearpygui()

# Flow graph window
def on_rx_node_link(sender, app_data):
    link_id_1, link_id_2 = app_data
    add_node_link(link_id_1, link_id_2, parent=sender)

def on_rx_node_delink(sender, app_data):
    link_id = app_data
    delete_item(link_id)

#================================================
#Setting Primary Window

with window(tag="Primary Window"):

#================================================
#Setting Window in Menu 
    with menu_bar():
        with menu(label="Settings"):

            with theme(tag= "close"):
                with theme_component():
                    add_theme_color(mvThemeCol_Text,(255, 64, 64))#Rot
                    add_theme_style(mvStyleVar_Alpha, 5)
                    
            add_menu_item(label="Toggle Fullscreen",callback= toggle_viewport_fullscreen)
            add_menu_item(label="Minimize",callback= minimize_viewport)
            add_menu_item(label="Close", callback= exit)
            bind_item_theme(last_item(),"close")

# #================================================
# # Flow Graph Window

# with window(label="RX DSP Flow Graph", width=800, height=400, pos=(25,25), tag="rx_win"):
#     with node_editor(callback=on_rx_node_link, delink_callback=on_rx_node_delink):
#         with node(label="USRP Source", pos=(20,100)):
#             with node_attribute(tag="src_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Signal from antenna")

#         with node(label="Clock Sync", pos=(200,200)):
#             with node_attribute(tag="clksync_in", attribute_type=mvNode_Attr_Input):
#                 add_text("Input")

#             with node_attribute(tag="clksync_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Synchronized")

#         with node(label="Equalizer", pos=(350,100)):
#             with node_attribute(tag="eq_in", attribute_type=mvNode_Attr_Input):
#                 add_text("Input")

#             with node_attribute(attribute_type=mvNode_Attr_Static):
#                 add_knob_float(label="Gain")

#             with node_attribute(tag="eq_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Equalized")

#         with node(label="Phase Locked Loop", pos=(600, 200)):
#             with node_attribute(tag="pll_in", attribute_type=mvNode_Attr_Input):
#                 add_text("Input")

#             with node_attribute(tag="pll_out", attribute_type=mvNode_Attr_Output):
#                 add_text("Locked")
#                 add_knob_float(label="Loop BW")


#         add_node_link(get_alias_id("src_out"), get_alias_id("clksync_in"))
#         add_node_link(get_alias_id("clksync_out"), get_alias_id("eq_in"))
#         add_node_link(get_alias_id("eq_out"), get_alias_id("pll_in"))

# #================================================
# Network plots Window

recv_plot = net.network_plot(url="udp://localhost:31415", dtype=float, nsamples=100, \
        label="Test", height=300, width=800)

plots = {
    # recv_plot: "plt_ampl"
}

# with window(label="Time domain plots", width=800, height=350, pos=(25,450)):
#     with recv_plot:
#         add_plot_axis(mvXAxis, label="Time")
#         add_plot_axis(mvYAxis, label="Amplitude", tag="axis")

#         add_line_series(recv_plot.xdata, recv_plot.ydata, parent="axis", tag="plt_ampl")

#================================================
# Byte Error Rate Window

#TO DO:BER von GNU Radio anzeigen 

with theme(tag= "ber_window"):
        with theme_component(mvAll):
            add_theme_style(mvStyleVar_WindowTitleAlign, 0.5)
            add_theme_style(mvStyleVar_WindowRounding, 5)
            add_theme_style(mvStyleVar_WindowBorderSize, 1)#Rad ein und aus Schalten 

with window(label="Byte Error Rate ", width=300, height=150, pos=(850,25),
    tag="__ber_id",no_title_bar = True, no_move=True, no_collapse= True) as ber_window : 
    add_text("The Byte Error Rate is:")    

    with theme(tag= "button_ber"):
        with theme_component(mvButton):
            add_theme_color(mvThemeCol_Button,(135, 206, 255))#Blau
            add_theme_color(mvThemeCol_Text,(0,0,0))#Schwarz
            add_theme_style(mvStyleVar_FrameRounding, 5)

    add_button(label="BER", height=50, width=150)
    bind_item_theme(last_item(),"button_ber")

bind_item_theme(ber_window,"ber_window")



#================================================
# Channel Window
#TO DO:
# recv_plot = net.network_plot(url="udp://localhost:31415", nsamples=100, label="Test", height=300, width=800)

# plots = {
#     recv_plot: "plt_ampl"
# }

# with window(label="Channel ", width=600, height=600, pos=(850,25)):
#     with child_window(autosize_x=True, height=100):
#         add_button(label="Toggle Fullscreen", callback= toggle_viewport_fullscreen)
#     with recv_plot:
#         add_plot_axis(mvXAxis, label="In-phase")
#         add_plot_axis(mvYAxis, label="Quadrature", tag="plt_ampl")

#         add_scatter_series(recv_plot.x_data, recv_plot.y_data, parent="plt_ampl")
# #================================================
# # Synchronized Window
# #TO DO:
# with window(label="Synchronized ", width=600, height=600, pos=(850,25)):
#     with child_window(autosize_x=True, height=100):
#         add_button(label="Toggle Fullscreen", callback= toggle_viewport_fullscreen)    

# #================================================
# # Equalized Window
# #TO DO:
# with window(label="Equalized ", width=600, height=600, pos=(850,25)):
#     with child_window(autosize_x=True, height=100):
#         add_button(label="Toggle Fullscreen", callback= toggle_viewport_fullscreen)   

# #================================================
# # Locked Window
# #TO DO:
# with window(label="Locked ", width=600, height=600, pos=(850,25)):
#     with child_window(autosize_x=True, height=100):
#         add_button(label="Toggle Fullscreen", callback= toggle_viewport_fullscreen)  




#================================================

# Start GUI and main loop

# Start window and main loop
show_viewport()
set_primary_window("Primary Window", True)

# Main loop
while is_dearpygui_running():
    for plt, tag in plots.items():
        plt.refresh_series(tag)

    render_dearpygui_frame()

#================================================
# Close everything

# clean up gui
destroy_context()
