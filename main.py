"""
Name: main.py
Authors: Logan Hoadley

This file intializes the tkinter environment, and contains functions related to the GUI, graph creation, and options.
"""
from tkinter import filedialog
import tkinter as tk
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from file_handler import is_wide_form, file_correct, long_to_wide
#from matplotlib.figure import Figure
# TODO:
#  Needs to be cleaned up to conform to PEP-8 Standards.
sns.set_theme(color_codes=True)


def openfile():
    """
    Called when user presses "Open File" from the navigation pane. Uses user-selected file and constructs a pandas
    dataframe containing its data, as well as a list of headers from that file. Then calls draw_options to populate
    the screen with relevant choices based on the file.
    :return:
    """
    global filepath, headers, firstRun, csv
    filepath = filedialog.askopenfilename(initialdir="%USERPROFILE%/Downloads",
                                          filetypes=(("Comma Separated Value Lists", "*.csv"), ("All Files", "*.*")))
    wide_data, headers = long_to_wide(filepath)
    csv = pd.DataFrame.from_records(wide_data)
    if firstRun:
        startLabel.pack_forget()
        firstRun = False
    else:
        clear_screen()
    draw_options()


# creates the buttons and visual elements necessary for interaction.
def draw_options():
    """
    Creates the elements for user manipulation in root. Reads the column field of the opened csv's dataframe and assigns
    those as options in a drop-down menu for user selection. Also generates options for user input, such as the order
    of the regression curve and robustness.
    :return:
    """
    global windowframe, buttonframe
    root.title(filepath)
    buttonframe = Frame(root)
    buttonframe.pack(side=LEFT)
    xaxis = StringVar()
    xaxis.set("X-axis")
    yaxis = StringVar()
    yaxis.set("Y-axis")
    windowframe = Frame(root)
    windowframe.pack(side=RIGHT)
    drop1 = OptionMenu(buttonframe, xaxis, *headers)
    drop1.pack(side=TOP)
    drop2 = OptionMenu(buttonframe, yaxis, *headers)
    drop2.pack(side=TOP)


    width = StringVar()
    robust = BooleanVar()
    robust.set(False)
    order = StringVar()
    islog = BooleanVar()
    range=StringVar()
    islog.set=(False)
    widthlabel = Label(buttonframe, text="Target Tread Width (mm): ")  # rename this option "tread deviation allowed" if absolute measure becomes available
    widthlabel.pack(side=TOP)
    widthinput = tk.Spinbox(buttonframe, from_=0, to=750, textvariable=width, wrap=False)
    widthinput.pack()
    devlabel = Label(buttonframe, text="Error allowed (mm): ")
    devlabel.pack()
    widthdeviation = tk.Spinbox(buttonframe, from_=1, to=10, textvariable=range, wrap=False)  # remove this option if absolute measure becomes available
    widthdeviation.pack()
    ordertext=tk.Label(buttonframe, text="Order of approximation:")
    ordertext.pack()
    orderinput = tk.Spinbox(buttonframe, from_=1, to=1000, textvariable=order, wrap=False)
    orderinput.pack()

    graphbutton = Button(buttonframe, text="Generate",
                         command=lambda: generate_graph(csv, xaxis.get(), yaxis.get(),
                                                        width.get(),robust.get(), islog.get(), order.get(), range.get()))  # remove range.get from this and generate_graph() if absolute measure becomes available.
    graphbutton.pack(side=BOTTOM)
    # outlier distributions are not compatible with a logarithmic function, so no argument is passed.
    outlierbutton = Button(buttonframe, text="Graph Outliers", command=lambda: graph_outliers(csv, xaxis.get(),
                                                                                              yaxis.get(),
                                                                                              order.get(), islog.get()))
    outlierbutton.pack(side=BOTTOM)

    logcheckbox = tk.Checkbutton(buttonframe, text="Logarithmic Approximation (overrides order!)", variable=islog,
                                 onvalue=True, offvalue=False)
    logcheckbox.pack(side=BOTTOM)
    robustcheck = tk.Checkbutton(buttonframe, text="Robust Analysis (overrides order!)", variable=robust, onvalue=True, offvalue=False)
    robustcheck.pack(side=BOTTOM)


def clear_screen():
    """
    Clears root in preparation to re-populate it with new options. Only called after firstrun = false, before which the
    instructional text is cleared. Clears buttonframe and windowframe.
    :return:
    """
    windowframe.pack_forget()
    buttonframe.pack_forget()


def generate_graph(dataframe, xaxis, yaxis, width, isrobust, islog, order, range):
    """
    Called when user presses 'Generate Graph," creates a toplevel window and populates it with the desired graph.
    :param dataframe: Pandas dataframe constructed from the user-selected .csv file in wide-form.
    :param xaxis: Selected parameter 1 that populates the x-axis. Variable of study.
    :param yaxis: Selected parameter 2 that populates the y-axis. Intended behavior uses tread width as control variable.
    :param width: Nominal width for tread, passed as a string.
    :param isrobust: Boolean, determines whether regplot ignores the effect of extreme outlying data points.
    :param islog: Boolean, determines if logarithmic analysis is performed. Overwrites order.
    :param order: Desired order of curve to fit to data set. If > 500, sets log = True for logarithmic approximation.
    :param range: Desired +/- variation allowed for visualization.
    :return:
    """
    global canvas
    width=int(width)
    order=int(order)
    range=int(range)
    graphwindow = Toplevel(height=900, width=1000)
    xjitter=dataframe[xaxis].mean()
    if islog or isrobust:
        order = 1 # order must be 1, the arguments are not compatible.
    fig = create_figure(dataframe, xaxis, yaxis, isrobust, order, islog,xjitter)
    if width != 0:
        plt.axhline(y=(width + range), color='r', linestyle='-')
        plt.axhline(y=(width - range), color='r', linestyle='-')
    #for use if tread deviation measure becomes available: (allows for large scale analysis)
    #if width!=0:
    #    plt.axhline(y=width, color='r', linestyle ='-')
    #    plt.axhline(y=*(-1*width), color='r', linestyle='-')
    canvas = FigureCanvasTkAgg(fig, master=graphwindow)
    canvas.draw()
    canvas.get_tk_widget().pack()
    button = tk.Button(graphwindow, text="Close", command=graphwindow.destroy)
    button.pack()

def create_figure(dataframe, xaxis, yaxis, isrobust, order, islog, xjitter):
    """
    Called by generate_graph() and .
    Generates a seaborn regression plot figure for use in a canvas, and to display to the user. This figure uses the
    selected parameters to generate a plot that displays the relation between the chosen parameter (x)
    and the tread width (y).
    :param dataframe: Pandas dataframe constructed from the user-selected .csv file in wide-form.
    :param xaxis: Selected parameter 1 that populates the x-axis. Variable of study.
    :param yaxis: Selected parameter 2 that populates the y-axis. Intended behavior uses tread width as control variable.
    :param isrobust: Boolean, determines whether regplot ignores the effect of extreme outlying data points.
    :param order: Desired order of curve to fit to data set. Overridden by islog = True, as the two are exclusionary.
    :param islog: Boolean, determines if curve fit uses logarithmic approximation. Overrides order number if set to True.
    :param xjitter: float, contains the mean of the selected x axis. Prevents the "stacking" of data by slightly shifting their values in visaulization only.
    :return f: Generated matplotlib.figure with a regression plot fit to the provided data.
    """
    f, dummy = plt.subplots(figsize=(6, 6))
    jitterval=0.0001*xjitter
    sns.regplot(x=xaxis, y=yaxis, data=dataframe, robust=isrobust, order=order, logx=islog, ci=99,x_jitter=jitterval, y_jitter=0.02)
    return f


def graph_outliers(dataframe, xaxis, yaxis, order, islog):
    """
    Called when user presses the "Graph Outliers" button. Handles the creation of the window for the generated
    graph to populate, processing of related arguments, and calls outlier_figure() to create that graph.
    :param dataframe: Pandas dataframe as assembled from the provided .csv, in wide form.
    :param xaxis: x-axis representing a column object in dataframe. Variable of study.
    :param yaxis: y-axis representing column object in dataframe. Expected to be tread width measurement.
    :param order: desired order of the fit regression curve.
    :param islog: Boolean, set to 1 if true. Less important in graphing outliers, but shares arg with the full graph.
    :return:
    """
    order=int(order)
    graphwindow = Toplevel(height=900, width=1000)
    if islog==True:
        order=1 #sets order to 1, to account for arbitrary order.

    fig = outlier_figure(dataframe, xaxis, yaxis, order)
    canvas = FigureCanvasTkAgg(fig, master=graphwindow)
    canvas.draw()
    canvas.get_tk_widget().pack()
    button = tk.Button(graphwindow, text="Close", command=graphwindow.destroy)
    button.pack()


def outlier_figure(dataframe, xaxis, yaxis, order):
    """
    Generates a relevant figure based on user selection, displaying outliers in the provided data set.
    :param dataframe: Pandas dataframe as assembled from the provided .csv, in wide form.
    :param xaxis: x-axis representing a column object in dataframe. Variable of study.
    :param yaxis: y-axis representing column object in dataframe. Expected to be tread width measurement.
    :param order: desired order of  fit regression curve.
    :return f: generated matplotlib.figure containing the outlying data points.
    """
    f, dummy = plt.subplots(figsize=(6, 6))
    sns.residplot(x=xaxis, y=yaxis, data=dataframe, lowess=True, order=order)
    return f

# Main
firstRun = True
root = tk.Tk() # necessary for tkinter
root.title("PyGuilin Dev Build")
main_menu = tk.Menu(root)
root.geometry("800x600")
root.config(menu=main_menu)
file_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=openfile)
file_menu.add_command(label="Export as...")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
startLabel = Label(root, text="Select File --> Open and select a valid CSV")
startLabel.pack()

root.mainloop()
