# matplotlib.pyplot.ion() enables interactive mode, which should serve the final product
from tkinter import filedialog
import tkinter as tk
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from file_handler import is_wide_form, file_correct, long_to_wide

# TODO:
#  Second pass on logarithmic function, and expanding order options to a numeric setting.
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
    clicked1 = StringVar()
    clicked1.set("Parameter 1")
    clicked2 = StringVar()
    clicked2.set("Parameter 2")
    windowframe = Frame(root)
    windowframe.pack(side=RIGHT)
    drop1 = OptionMenu(buttonframe, clicked1, *headers)
    drop1.pack(side=TOP)
    drop2 = OptionMenu(buttonframe, clicked2, *headers)
    drop2.pack(side=TOP)
    sliderlabel = Label(buttonframe, text="Width deviation limit in\n tenths of millimeters: ")
    sliderlabel.pack(side=TOP)
    limit = DoubleVar()
    robust = BooleanVar()
    robust.set(False)
    order = IntVar()
    order.set(1)

    slider = Scale(buttonframe, from_=0, to=75, orient=HORIZONTAL, variable=limit)
    slider.pack(side=TOP)
    # maybe replace sider with an input field, so user can just type in a value
    # add: button or tickbox to graph 2nd order
    # add: entry for confidence interval

    robustcheck = tk.Checkbutton(buttonframe, text="Robust Analysis", variable=robust, onvalue=True, offvalue=False)
    robustcheck.pack(side=TOP)
    graphbutton = Button(buttonframe, text="Generate",
                         command=lambda: generate_graph(csv, clicked1.get(), clicked2.get(),
                                                        limit.get(),robust.get(), order.get()))
    graphbutton.pack(side=BOTTOM)
    outlierbutton = Button(buttonframe, text="Graph Outliers", command=lambda: graph_outliers(csv, clicked1.get(),
                                                                                              clicked2.get(),
                                                                                              order.get()))
    outlierbutton.pack(side=BOTTOM)
    strucbutton1 = Radiobutton(buttonframe, text="Linear Approximation", variable=order, value=1)
    strucbutton1.pack()
    strucbutton2 = Radiobutton(buttonframe, text="Quadratic Approximation", variable=order, value=2)
    strucbutton2.pack()
    logbutton = Radiobutton(buttonframe, text="Logarithmic Approximation", variable=order, value=999)
    logbutton.pack()


def clear_screen():
    """
    Clears root in preparation to re-populate it with new options. Only called after firstrun = false, before which the
    instructional text is cleared. Clears buttonframe and windowframe.
    :return:
    """
    windowframe.pack_forget()
    buttonframe.pack_forget()


def generate_graph(dataframe, xaxis, yaxis, limit, isrobust, order):
    """
    Called when user presses 'Generate Graph," creates a toplevel window and populates it with the desired graph.
    :param dataframe: Pandas dataframe constructed from the user-selected .csv file in wide-form.
    :param xaxis: Selected parameter 1 that populates the x-axis. Variable of study.
    :param yaxis: Selected parameter 2 that populates the y-axis. Intended behavior uses tread width as control variable.
    :param limit: Desired limit for width tolerance, determining the height of a horizontal line to be drawn for reference.
    :param isrobust: Boolean, determines whether regplot ignores the effect of extreme outlying data points.
    :param order: Desired order of curve to fit to data set. If > 500, sets log = True for logarithmic approximation.
    :return:
    """
    global canvas
    graphwindow = Toplevel(height=900, width=1000)
    if order > 500:
        log = True
        order = 1
    else:
        log = False
    fig = create_figure(dataframe, xaxis, yaxis, isrobust, order, log)
    if limit != 0:
        plt.axhline(y=(limit / 1000), color='r', linestyle='-')
    canvas = FigureCanvasTkAgg(fig, master=graphwindow)
    canvas.draw()
    canvas.get_tk_widget().pack()
    button = tk.Button(graphwindow, text="Close", command=graphwindow.destroy)
    button.pack()

def create_figure(dataframe, xaxis, yaxis, isrobust, order, islog):
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
    :return f: Generated matplotlib.figure with a regression plot fit to the provided data.
    """
    f, dummy = plt.subplots(figsize=(6, 6))
    sns.regplot(x=xaxis, y=yaxis, data=dataframe, robust=isrobust, order=order, logx=islog, ci=95)
    return f


def graph_outliers(dataframe, xaxis, yaxis, order):
    """
    Called when user presses the "Graph Outliers" button. Handles the creation of the window for the generated
    graph to populate, processing of related arguments, and calls outlier_figure() to create that graph.
    :param dataframe: Pandas dataframe as assembled from the provided .csv, in wide form.
    :param xaxis: x-axis representing a column object in dataframe. Variable of study.
    :param yaxis: y-axis representing column object in dataframe. Expected to be tread width measurement.
    :param order: desired order of the fit regression curve.
    :return:
    """
    graphwindow = Toplevel(height=900, width=1000)
    if order > 500:
        order = 1

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
