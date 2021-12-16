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
#show_demo()


#================================================
# Globl variables

ber_win_tag = "ber_window"
ber_win_pos = (0,25)
ber_win_width = 800 
ber_win_height = 160

# Network Plots
time_plot         = net.network_plot(url="udp://localhost:31415", dtype=float, \
                        nsamples=500, tag="time_plot", label="Time plot")
channel_plot      = net.network_constellation_plot(url="udp://localhost:31416", \
                        nsamples=512, tag="channel_plot", label="Channel")
synchronized_plot = net.network_constellation_plot(url="udp://localhost:31417", \
                        nsamples=512, tag="synchronized_plot",  label="Synchronized")
equalized_plot    = net.network_constellation_plot(url="udp://localhost:31418", \
                        nsamples=512, tag="equalized_plot",  label="Equalized")
locked_plot       = net.network_constellation_plot(url="udp://localhost:31419", \
                        nsamples=512, tag="locked_plot",  label="Locked")

constellation_plots = [channel_plot, synchronized_plot, equalized_plot, locked_plot]
network_plots = [time_plot] + constellation_plots

const_plots_start     = (800, 25)
const_plot_win_width  = 560
const_plot_win_height = 560

# size of the plot windows
plot_window_sizes = {
    time_plot: (800, 400),

    channel_plot:      (const_plot_win_width, const_plot_win_height),
    synchronized_plot: (const_plot_win_width, const_plot_win_height),
    equalized_plot:    (const_plot_win_width, const_plot_win_height),
    locked_plot:       (const_plot_win_width, const_plot_win_height),
}

# Where to place the network plot windows
plot_window_positions = {
    time_plot:         (0,185),
    channel_plot:      (const_plots_start),
    synchronized_plot: (const_plots_start[0] + const_plot_win_width, \
                        const_plots_start[1]),
    equalized_plot:    (const_plots_start[0], \
                        const_plots_start[1] + const_plot_win_height),
    locked_plot:       (const_plots_start[0] + const_plot_win_width, \
                        const_plots_start[1] + const_plot_win_height),
}

# Wheter contellation plots axes are locked
plots_locked = True

#================================================
# Set up theme and looks

# Font
with font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = add_font("res/ttf/Hack-Regular.ttf", 20)
    # second_font = add_font("NotoSerifCJKjp-Medium.otf", 10)
    # test = add_font("NotoSerifCJKjp-Medium.otf", 30)

# Constellation diagrams
with theme(tag="constellation_series_theme"):
    with theme_component(mvScatterSeries):
        add_theme_style(mvPlotStyleVar_Marker, mvPlotMarker_Asterisk, category=mvThemeCat_Plots)
        add_theme_style(mvPlotStyleVar_MarkerSize, 3, category=mvThemeCat_Plots)
    with theme_component(mvAll):
        add_theme_style(mvStyleVar_WindowBorderSize,0)

#================================================
# GUI Callback functions

# Menu Bar 
def exit(sender, data):
    stop_dearpygui()

#================================================
# Primary Window

with window(tag="primary_window"):
    # Grössere Schrifftart/ Grösse für das ganze Dokument definiert
    bind_font(default_font) 

    with menu_bar():
        with menu(label="Settings"):
            add_menu_item(label="Toggle Fullscreen", callback=toggle_viewport_fullscreen)
            add_menu_item(label="Minimize", callback=minimize_viewport)
            add_menu_item(label="Close", callback=exit, tag="menu_settings_close")

            with theme(tag="close"):
                with theme_component():
                    add_theme_color(mvThemeCol_Text,(255, 64, 64))
                    add_theme_style(mvStyleVar_Alpha, 5)
            bind_item_theme("menu_settings_close", "close")

        with menu(label="Windows"):
            def restore_windows():
                global plot_window_sizes, plot_window_positions

                configure_item(ber_win_tag,
                    width=ber_win_width,
                    height=ber_win_height,
                    pos=ber_win_pos)

                for plot in network_plots:
                    configure_item(plot.window_tag,
                            width=plot_window_sizes[plot][0],
                            height=plot_window_sizes[plot][1],
                            pos=plot_window_positions[plot])

            add_menu_item(label="Restore Default Positions", callback=restore_windows)

            def unlock_plots():
                global plots_locked
                if plots_locked:
                    for plot in constellation_plots:
                        set_axis_limits_auto(plot.xaxis_tag)
                        set_axis_limits_auto(plot.yaxis_tag)
                else:
                    for plot in constellation_plots:
                        set_axis_limits(plot.xaxis_tag, -2, 2)
                        set_axis_limits(plot.yaxis_tag, -2, 2)

                plots_locked = not plots_locked

            add_menu_item(label="Unlocked plots", callback=unlock_plots, check=True)



#================================================
# Flow Graph Window

def add_and_load_image(image_path, **kwargs):
    width, height, channels, data = load_image(image_path)

    with texture_registry() as reg_id:
        texture_id = add_static_texture(width, height, data, parent=reg_id)
    return add_image(texture_id, **kwargs)


with window(label="RX DSP Flow Graph", width=800, height=653, pos=(0,585),\
 no_collapse=True, no_close=True,no_title_bar= True, no_scrollbar=True,\
 no_move=True,no_resize=True) as png:
    add_and_load_image("res/pic/overview.png", width=650, height=531, pos=(50,0))
    bind_item_theme(png, "constellation_series_theme") 

# with window(label="RX DSP Flow Graph", width=800, height=400, pos=(0,25), tag="rx_win"):
#     add_text("TODO:Blockschaltbild")
#     with node_editor():
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
# Network plots

def make_constellation_plot_window(plot, label):
    with window(label=label, no_collapse=True, no_close=True,no_title_bar= True,no_move=True,no_resize=True, \
            width=plot_window_sizes[plot][0], \
            height=plot_window_sizes[plot][1], \
            pos=plot_window_positions[plot], \
            tag=plot.window_tag) as constelation:
        with plot:
            # Fit to width of window
            configure_item(plot.tag, width=-1, height=-1)

            # Create and configure axis
            add_plot_axis(mvXAxis, label="In-Phase", tag=plot.xaxis_tag)
            add_plot_axis(mvYAxis, label="Quadrature", tag=plot.yaxis_tag)

            add_plot_legend()
            set_axis_limits(plot.xaxis_tag, -2, 2)
            set_axis_limits(plot.yaxis_tag, -2, 2)

            # Add series from network
            add_scatter_series(plot.xdata, plot.ydata, \
                label=label, parent=plot.xaxis_tag, tag=plot.series_tag)
            bind_item_theme(plot.series_tag, "constellation_series_theme")
        bind_item_theme(constelation, "constellation_series_theme")

make_constellation_plot_window(channel_plot, "Channel")
make_constellation_plot_window(synchronized_plot, "Synchronized")
make_constellation_plot_window(equalized_plot, "Equalized")
make_constellation_plot_window(locked_plot, "Locked")

with window(label="Time domain", width=800, height=400, pos=(0,185), \
            no_title_bar= True,no_move=True,no_resize=True,no_collapse=True, no_close=True,\
            tag=time_plot.window_tag) as time:
    with time_plot:
        configure_item(time_plot.tag, width=-1, height=-1)

        add_plot_axis(mvXAxis, label="Time", tag=time_plot.xaxis_tag)
        add_plot_axis(mvYAxis, label="Amplitude", tag=time_plot.yaxis_tag)
        add_line_series(time_plot.xdata, time_plot.ydata, parent=time_plot.xaxis_tag, tag=time_plot.series_tag)
    bind_item_theme(time, "constellation_series_theme")
#================================================
# Bit Error Rate Window

#TO DO:BER von GNU Radio anzeigen 

with theme(tag="theme_ber_window"):
        with theme_component(mvAll):
            add_theme_style(mvStyleVar_WindowTitleAlign, 0.5)
            add_theme_style(mvStyleVar_WindowBorderSize, 0)#Rad ein und aus Schalten 

with window(label="Bit Error Rate ", width=800, height=160, pos=(0,25),\
    no_collapse=True, no_close=True, no_title_bar= True,no_move=True,no_resize=True,\
    tag=ber_win_tag) as ber_window:
        add_text("The Bit Error Rate is:",pos=(50,25))
        with theme(tag="button_ber"):
            with theme_component(mvButton):
                add_theme_color(mvThemeCol_Button,(135, 206, 255)) #Blau
                add_theme_color(mvThemeCol_Text,(0,0,0)) #Schwarz
                add_theme_style(mvStyleVar_FrameRounding, 5)

        add_button(label="BER", height=60, width=700, pos=(50,70), tag="ber_value")
        bind_item_theme(last_item(), "button_ber")
        bind_item_theme(ber_window, "theme_ber_window")

def set_ber(values):
    ber_curr, ber_max, ber_avg = values
    configure_item("ber_value", label=f"Current: {ber_curr}, Max: {ber_max}, Avg: {ber_avg}")

ber_value = net.network_value(url="udp://localhost:31420", dtype=float, refresh_func=set_ber)


#================================================
# Start GUI and main loop

# Start window and main loop
show_viewport()
set_primary_window("primary_window", True)

# Main loop
while is_dearpygui_running():
    for plt in network_plots:
        plt.refresh_series(plt.series_tag)
    ber_value.refresh()

    render_dearpygui_frame()

#================================================
# Close everything

# clean up gui
destroy_context()
