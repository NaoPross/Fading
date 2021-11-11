from dearpygui.core import *
from dearpygui.simple import *
from math import cos

def plot_callback(sender, data):
    # keeping track of frames
    frame_count = get_data("frame_count")
    frame_count += 1
    add_data("frame_count", frame_count)

    # updating plot data
    plot_datax = get_data("plot_datax")
    plot_datay = get_data("plot_datay")
    if len(plot_datax) > 2000:
        frame_count = 0
        plot_datax.clear()
        plot_datay.clear()
    plot_datax.append(3.14 * frame_count / 180)
    plot_datay.append(cos(3 * 3.14 * frame_count / 180))
    add_data("plot_datax", plot_datax)
    add_data("plot_datay", plot_datay)

    # plotting new data
    add_line_series("Plot", "Cos", plot_datax, plot_datay, weight=2)

with window("Tutorial", width=500, height=500):
    add_plot("Plot", height=-1)
    add_data("plot_datax", [])
    add_data("plot_datay", [])
    add_data("frame_count", 0)
    add_input_text("freq")
    with menu_bar("Main Menu Bar"):
        with menu("File"):
            add_menu_item("test")
    set_render_callback(plot_callback)

with window("Heat", width=500, height=500):
    add_plot("HeatPlot", show_color_scale=False, scale_min=0.0, scale_max=6.0, 
                         scale_height=400, no_legend=True, 
                         no_mouse_pos=True, xaxis_lock_min=True, xaxis_lock_max=True, xaxis_no_gridlines=True, xaxis_no_tick_marks=True,
                         yaxis_no_gridlines=True, yaxis_no_tick_marks=True, yaxis_lock_min=True, yaxis_lock_max=True, height=400)
    set_color_map("HeatPlot", 6)
    values = [0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0,
                          2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0,
                          1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0,
                          0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0,
                          0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0,
                          1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1,
                          0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]
    add_heat_series("HeatPlot", "heat data", values, 7, 7, 0, 6, format='')
    

start_dearpygui()