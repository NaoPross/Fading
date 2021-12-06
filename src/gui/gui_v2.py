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
create_viewport(title="Fading Demonstrator",width=1920, height=1200)
setup_dearpygui()

# Show demo for dev
show_demo()
#show_font_manager()

#================================================
# add a font registry
with font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = add_font("NotoSerifCJKjp-Medium.otf", 20)
    second_font = add_font("NotoSerifCJKjp-Medium.otf", 10)
    test = add_font("NotoSerifCJKjp-Medium.otf", 30)
    
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

# add and load images
def add_and_load_image(image_path):
    width, height, channels, data = load_image(image_path)

    with texture_registry() as reg_id:
        texture_id = add_static_texture(width, height, data, parent=reg_id)

    return add_image(texture_id)


#================================================
#Setting Primary Window

with window(tag="Primary Window"):
    bind_font(default_font) # Grössere Schrifftart/ Grösse für das ganze Dokument definiert

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

        with menu(label="Plot"):
            add_menu_item(label="unlock x limits", callback=lambda: set_axis_limits_auto("xaxis_channel"))    
            add_menu_item(label="unlock y limits", callback=lambda: set_axis_limits_auto("yaxis_channel"))


#================================================
# Flow Graph Window

with window(label="RX DSP Flow Graph", width=800, height=400, pos=(0,25), tag="rx_win", 
    no_title_bar = True, no_move=True, no_collapse= True):
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
    # recv_plot: "plt_ampl"
}

with window(label="Time domain plots", width=800, height=350, pos=(0,425),
    no_title_bar = True, no_move=True, no_collapse= True):
    with recv_plot:
        add_plot_axis(mvXAxis, label="Time")
        add_plot_axis(mvYAxis, label="Amplitude", tag="axis")

        add_line_series(recv_plot.xdata, recv_plot.ydata, parent="axis", tag="plt_ampl")

#================================================
# Byte Error Rate Window

#TO DO:BER von GNU Radio anzeigen 

with theme(tag= "ber_window"):
        with theme_component(mvAll):
            add_theme_style(mvStyleVar_WindowTitleAlign, 0.5)
            add_theme_style(mvStyleVar_WindowRounding, 5)
            add_theme_style(mvStyleVar_WindowBorderSize, 1)#Rad ein und aus Schalten 

with window(label="Byte Error Rate ", width=300, height=150, pos=(1200,875)
    ,no_title_bar = True, no_move=True, no_collapse= True) as ber_window : 

    add_text("The Byte Error Rate is:",pos=(35,10))    

    with theme(tag= "button_ber"):
        with theme_component(mvButton):
            add_theme_color(mvThemeCol_Button,(135, 206, 255))#Blau
            add_theme_color(mvThemeCol_Text,(0,0,0))#Schwarz
            add_theme_style(mvStyleVar_FrameRounding, 5)

    add_button(label="BER", height=60, width=150,pos=(75,60))
    bind_item_theme(last_item(),"button_ber")

bind_item_theme(ber_window,"ber_window")
bind_item_font(ber_window,test)

#================================================
# Picture Window
with window(label="Picture", width=400, height=300, pos=(0,825),
    no_title_bar = True, no_move=True, no_collapse= True) as picture_window : 
    #with child_window(width=400, height=400):
    add_and_load_image("logo.png")
    add_text("Picture 1")
    #add_and_load_image("lena512color.png") #TO DO Problem lösen 

with window(label="Picture_2", width=400, height=300, pos=(400,825),
    no_title_bar = True, no_move=True, no_collapse= True) as picture_window : 
    #with child_window(width=400, height=400):
    add_and_load_image("logo.png")
    add_text("Picture 2")
    #add_and_load_image("l

#================================================
# Channel Window
# TO DO: Change Data to Real Data from the GUI 

# Some Data to plot 
sindatax = []
sindatay = []
for i in range(-2, 100):
    sindatax.append(i / 100)
    sindatay.append(0.5 + 0.5 * np.sin(50 * i / 100))
sindatay2 = []
for i in range(-2, 100):
    sindatay2.append(2 + 0.5 * np.sin(50 * i / 100))

with window(label="Channel ", width=560, height=400, pos=(800,25),
    no_title_bar = True, no_move=True, no_collapse= True):

    # create a theme for the plot
    with theme(tag="plot_theme"):
        with theme_component(mvScatterSeries):
            add_theme_color(mvPlotCol_Line, (135, 206, 255), category=mvThemeCat_Plots)
            add_theme_style(mvPlotStyleVar_Marker,mvPlotMarker_Asterisk, category=mvThemeCat_Plots) #TO DO: change to mvPlotMarker_Circle
            add_theme_style(mvPlotStyleVar_MarkerSize, 3, category=mvThemeCat_Plots)

    # Plot
    with plot(tag="plot", label="Channel", height=-1, width=-1):

        # optionally create legend
        add_plot_legend()

        # REQUIRED: create x and y axes
        add_plot_axis(mvXAxis, label="In-phase",tag="xaxis_channel")
        set_axis_limits("xaxis_channel", -2, 2)

        add_plot_axis(mvYAxis, label= "Quadrature", tag="yaxis_channel")
        set_axis_limits("yaxis_channel", -2, 2)

        # series belong to a y axis
        add_scatter_series(sindatax, sindatay2, label="Some Data", parent="yaxis_channel", tag="series_data2")
        #add_button(label="Delete Series 1", parent=last_item(), callback=lambda: delete_item("series_data2"))

        # apply theme to series
        bind_item_theme("series_data2", "plot_theme")
  


#================================================
# Synchronized Window
with window(label="Synchronized", width=560, height=400, pos=(1360,25),
    no_title_bar = True, no_move=True, no_collapse= True):
    add_text("TO DO Synchronized")

    # with child_window(autosize_x=True, height=100):
    #     add_button(label="Toggle Fullscreen", callback= toggle_viewport_fullscreen)
# #================================================
# # Equalized Window
with window(label="Equalized", width=560, height=400, pos=(800,425),
    no_title_bar = True, no_move=True, no_collapse= True):
    add_text("TO DO Equalized")

#================================================
# Locked Window
# TO DO: Change Data to Real Data from the GUI 

# Some Data to plot 
sindatax = []
sindatay = []
for i in range(-2, 100):
    sindatax.append(i / 100)
    sindatay.append(0.5 + 0.5 * np.sin(50 * i / 100))
sindatay2 = []
for i in range(-2, 100):
    sindatay2.append(2 + 0.5 * np.sin(50 * i / 100))

with window(label="Locked ", width=560, height=400, pos=(1360,425),
    no_title_bar = True, no_move=True, no_collapse= True):

    # create a theme for the plot
    with theme(tag="plot_theme_locked"):
        with theme_component(mvScatterSeries):
            add_theme_color(mvPlotCol_Line, (135, 206, 255), category=mvThemeCat_Plots)
            add_theme_style(mvPlotStyleVar_Marker,mvPlotMarker_Asterisk, category=mvThemeCat_Plots) #TO DO: change to mvPlotMarker_Circle
            add_theme_style(mvPlotStyleVar_MarkerSize, 3, category=mvThemeCat_Plots)

    # Plot
    with plot(tag="plot_locked", label="Locked", height=-1, width=-1):

        # optionally create legend
        add_plot_legend()

        # REQUIRED: create x and y axes
        add_plot_axis(mvXAxis, label="In-phase",tag="xaxis_locked")
        set_axis_limits("xaxis_locked", -2, 2)

        add_plot_axis(mvYAxis, label= "Quadrature", tag="yaxis_locked")
        set_axis_limits("yaxis_locked", -2, 2)

        # series belong to a y axis
        add_scatter_series(sindatax, sindatay2, label="Some Data", parent="yaxis_locked", tag="series_data2_locked")
        #add_button(label="Delete Series 1", parent=last_item(), callback=lambda: delete_item("series_data2"))

        # apply theme to series
        bind_item_theme("series_data2_locked", "plot_theme_locked")

#TO DO: find a better way to do that 
    with group(horizontal=True):
        add_button(label="unlock x limits", callback=lambda: set_axis_limits_auto("xaxis_locked"))
        add_button(label="unlock y limits", callback=lambda: set_axis_limits_auto("yaxis_locked"))
        




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
