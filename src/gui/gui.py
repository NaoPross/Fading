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
show_documentation()


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
#Setting Window Test 
# with window(label="Dear", width=800, height=800, on_close=_on_demo_close, pos=(100, 100)):
    
    with menu_bar():
        with menu(label="Settings"):
            add_menu_item(label="Option 1", callback=_log)
            add_menu_item(label="Option 2", check=True, callback=_log)
            add_menu_item(label="Option 3", check=True, default_value=True, callback=_log)





# Settings Window
def exit(sender, data):
    stop_dearpygui()

# def _hsv_to_rgb(h, s, v):
#     if s == 0.0: return (v, v, v)
#     i = int(h*6.) # XXX assume int() truncates!
#     f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
#     if i == 0: return (255*v, 255*t, 255*p)
#     if i == 1: return (255*q, 255*v, 255*p)
#     if i == 2: return (255*p, 255*v, 255*t)
#     if i == 3: return (255*p, 255*q, 255*v)
#     if i == 4: return (255*t, 255*p, 255*v)
#     if i == 5: return (255*v, 255*p, 255*q)

with window(label="Settings", width=200, height=400, pos=(25, 25), tag="sim_win",
 no_close=True,no_background= True):
    with menu_bar():
        with menu(label="Settings"):
            add_menu_item(label="Option 1")
            add_menu_item(label="Option 2", check=True)
            add_menu_item(label="Option 3", check=True, default_value=True)

    #Farbwahl in schleife und mit def?
    with theme(tag= "button_window"):
        with theme_component(mvButton):
            add_theme_color(mvThemeCol_Button,(135, 206, 255))#Blau
            add_theme_color(mvThemeCol_Text,(0,0,0))#Schwarz
            add_theme_style(mvStyleVar_FrameRounding, 5)

    add_button(label="Toggle Fullscreen", height=50, width=150,callback= toggle_viewport_fullscreen)
    bind_item_theme(last_item(),"button_window")

    with theme(tag= "button_minimize"):
        with theme_component(mvButton):
            #add_theme_color(mvThemeCol_Button,(135, 206, 255))#Blau
            #add_theme_color(mvThemeCol_Text,(0,0,0))#Schwarz
            add_theme_style(mvStyleVar_FrameRounding, 5)
    add_button(label="Minimize",height=50, width=150, callback= minimize_viewport)
    bind_item_theme(last_item(),"button_minimize")
    
    #with child_window(autosize_x=True, height=100)as close:
    add_button(label="Maximize",height=50, width=150, callback= maximize_viewport) #Befehl nötig ? 
    
    with theme(tag= "button_close"):
        with theme_component(mvButton):
            add_theme_color(mvThemeCol_Button,(255, 64, 64))#Rot
            add_theme_color(mvThemeCol_Text,(0,0,0))#Schwarz
            add_theme_style(mvStyleVar_FrameRounding, 5)

    add_button(label="Close", height=50, width=150, callback= exit) 
    bind_item_theme(last_item(),"button_close")

        


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

with window(label="Time domain plots", width=800, height=350, pos=(25,450)):
    with recv_plot:
        add_plot_axis(mvXAxis, label="Time")
        add_plot_axis(mvYAxis, label="Amplitude", tag="axis")

        add_line_series(recv_plot.xdata, recv_plot.ydata, parent="axis", tag="plt_ampl")

#================================================
# Byte Error Rate Window
#TO DO:

with window(label="Byte Error Rate ", width=300, height=150, pos=(850,25),tag="__ber_id",no_move=True, no_collapse= True):
     add_text("The Byte Error Rate is:")    


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

# Main loop
while is_dearpygui_running():
    for plt, tag in plots.items():
        plt.refresh_series(tag)

    render_dearpygui_frame()

#================================================
# Close everything

# clean up gui
destroy_context()