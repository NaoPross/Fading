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
show_debug()

#================================================
# Set up theme and looks

# Font
# with font_registry():
#     # first argument ids the path to the .ttf or .otf file
#     default_font = add_font("NotoSerifCJKjp-Medium.otf", 20)
#     second_font = add_font("NotoSerifCJKjp-Medium.otf", 10)
#     test = add_font("NotoSerifCJKjp-Medium.otf", 30)

# Constellation diagrams
with theme(tag="constellation_series_theme"):
    with theme_component(mvScatterSeries):
        # add_theme_style(mvPlotStyleVar_Marker, mvPlotMarker_Asterisk, category=mvThemeCat_Plots)
        add_theme_style(mvPlotStyleVar_MarkerSize, 3, category=mvThemeCat_Plots)


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
    # do nothing
    # delete_item(link_id)

# add and load images
def add_and_load_image(image_path):
    width, height, channels, data = load_image(image_path)

    with texture_registry() as reg_id:
        texture_id = add_static_texture(width, height, data, parent=reg_id)

    return add_image(texture_id)


#================================================
# Primary Window

with window(tag="primary_window"):
    # Grössere Schrifftart/ Grösse für das ganze Dokument definiert
    # bind_font(default_font) 

    with menu_bar():
        with menu(label="Settings"):
            add_menu_item(label="Toggle Fullscreen",callback=toggle_viewport_fullscreen)
            add_menu_item(label="Minimize",callback=minimize_viewport)
            add_menu_item(label="Close", callback=exit)

            with theme(tag="close"):
                with theme_component():
                    add_theme_color(mvThemeCol_Text,(255, 64, 64))
                    add_theme_style(mvStyleVar_Alpha, 5)
            bind_item_theme(last_item(),"close")

#================================================
# Flow Graph Window

with window(label="RX DSP Flow Graph", width=800, height=400, pos=(0,25), tag="rx_win"):
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

#================================================
# Network plots

time_plot         = net.network_plot(url="udp://localhost:31415", dtype=float, \
                        nsamples=100, tag="time_plot", label="Time plot")
channel_plot      = net.network_constellation_plot(url="udp://localhost:31416", \
                        nsamples=80, tag="channel_plot", label="Channel")
synchronized_plot = net.network_constellation_plot(url="udp://localhost:31417", \
                        nsamples=100, tag="synchronized_plot",  label="Synchronized")
equalized_plot    = net.network_constellation_plot(url="udp://localhost:31418", \
                        nsamples=100, tag="equalized_plot",  label="Equalized")
locked_plot       = net.network_constellation_plot(url="udp://localhost:31419", \
                        nsamples=100, tag="locked_plot",  label="Locked")

network_plots = {
    time_plot:         "time_plot_series",
    channel_plot:      "channel_plot_series",
    synchronized_plot: "synchronized_plot_series",
    equalized_plot:    "equalized_plot_series",
    locked_plot:       "locked_plot_series",
}

with window(label="Time domain", width=800, height=350, pos=(0,425)):
    with time_plot:
        add_plot_axis(mvXAxis, label="Time", tag="xaxis_time")
        add_plot_axis(mvYAxis, label="Amplitude", tag="yaxis_time")
        add_line_series(time_plot.xdata, time_plot.ydata, parent="yaxis_time", tag=network_plots[time_plot])

with window(label="Channel", width=560, height=400, pos=(800,25)):
    with channel_plot:
        add_plot_axis(mvXAxis, label="In-Phase", tag="inphase_channel")
        add_plot_axis(mvYAxis, label="Quadrature", tag="quadrature_channel")

        add_plot_legend()
        set_axis_limits("inphase_channel", -2.5, 2.5)
        set_axis_limits("quadrature_channel", -2.5, 2.5)

        series_tag = network_plots[channel_plot]
        add_scatter_series(channel_plot.xdata, channel_plot.ydata, \
            label = "Channel", parent="inphase_channel", tag=series_tag)
        bind_item_theme(series_tag, "constellation_series_theme")
        # bind_colormap("channel_plot", mvPlotColormap_Spectral)

with window(label="Synchronized", width=560, height=400, pos=(1360,25)):
    with synchronized_plot:
        add_plot_axis(mvXAxis, label="In-Phase", tag="inphase_synchronized")
        add_plot_axis(mvYAxis, label="Quadrature", tag="quadrature_synchronized")

        add_plot_legend()
        set_axis_limits("inphase_synchronized", -2.5, 2.5)
        set_axis_limits("quadrature_synchronized", -2.5, 2.5)

        series_tag = network_plots[synchronized_plot]
        add_scatter_series(synchronized_plot.xdata, synchronized_plot.ydata, \
            label="Synchronized", parent="inphase_synchronized", tag=series_tag)
        bind_item_theme(series_tag, "constellation_series_theme")

with window(label="Equalized", width=560, height=400, pos=(800,425)):
    with equalized_plot:
        add_plot_legend()
        add_plot_axis(mvXAxis, label="In-Phase", tag="inphase_equalized")
        add_plot_axis(mvYAxis, label="Quadrature", tag="quadrature_equalized")

        add_plot_legend()
        set_axis_limits("inphase_equalized", -1.5, 1.5)
        set_axis_limits("quadrature_equalized", -1.5, 1.5)

        series_tag = network_plots[equalized_plot]
        add_scatter_series(equalized_plot.xdata, equalized_plot.ydata, \
            label="Equalized", parent="inphase_equalized", tag=series_tag)
        bind_item_theme(series_tag, "constellation_series_theme")

with window(label="Locked", width=560, height=400, pos=(1360,425)):
    with locked_plot:
        add_plot_legend()
        add_plot_axis(mvXAxis, label="In-Phase", tag="inphase_locked")
        add_plot_axis(mvYAxis, label="Quadrature", tag="quadrature_locked")

        add_plot_legend()
        set_axis_limits("inphase_locked", -1.5, 1.5)
        set_axis_limits("quadrature_locked", -1.5, 1.5)

        series_tag = network_plots[locked_plot]
        add_scatter_series(locked_plot.xdata, locked_plot.ydata, \
            label="Locked", parent="inphase_locked", tag=series_tag)
        bind_item_theme(series_tag, "constellation_series_theme")

#================================================
# Bit Error Rate Window

#TO DO:BER von GNU Radio anzeigen 

with theme(tag= "ber_window"):
        with theme_component(mvAll):
            add_theme_style(mvStyleVar_WindowTitleAlign, 0.5)
            add_theme_style(mvStyleVar_WindowRounding, 5)
            add_theme_style(mvStyleVar_WindowBorderSize, 1)#Rad ein und aus Schalten 

with window(label="Bit Error Rate ", width=300, height=150, pos=(1200,875), no_title_bar = True, no_move=True, no_collapse= True) as ber_window : 

    add_text("The Bit Error Rate is:", pos=(35,10))

    with theme(tag= "button_ber"):
        with theme_component(mvButton):
            add_theme_color(mvThemeCol_Button,(135, 206, 255))#Blau
            add_theme_color(mvThemeCol_Text,(0,0,0))#Schwarz
            add_theme_style(mvStyleVar_FrameRounding, 5)

    add_button(label="BER", height=60, width=150,pos=(75,60))
    bind_item_theme(last_item(),"button_ber")

# bind_item_theme(ber_window, "ber_window")
# bind_item_font(ber_window, test)

#================================================
# Picture Window
with window(label="Picture", width=400, height=300, pos=(0,825)) as picture_window : 
    add_and_load_image("lena512color.png") #TO DO Problem lösen 

#================================================
# Start GUI and main loop

# Start window and main loop
show_viewport()
set_primary_window("primary_window", True)

# Main loop
while is_dearpygui_running():
    for plt, tag in network_plots.items():
        plt.refresh_series(tag)

    render_dearpygui_frame()

#================================================
# Close everything

# clean up gui
destroy_context()
