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
# TODO: Needs to be cleaned up to conform to PEP-8 Standards.
sns.set_theme(color_codes=True)


def openfile():
    global filepath, headers, firstRun, csv
    filepath = filedialog.askopenfilename(initialdir="%USERPROFILE%/Downloads",
                                          filetypes=(("Comma Separated Value Lists", "*.csv"), ("All Files", "*.*")))
    wide_data, headers = long_to_wide(filepath)
    csv = pd.DataFrame.from_records(wide_data)
    if firstRun:
        startLabel.pack_forget()
        firstRun = False
    else:
        undraw()
    draw()


# creates the buttons and visual elements necessary for interaction.
def draw():
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
    graphbutton = Button(buttonframe, text="Generate", command=lambda: graph(csv, clicked1.get(),
                                                                             clicked2.get(), limit.get(), robust.get(), order.get()))
    graphbutton.pack(side=BOTTOM)
    outlierbutton = Button(buttonframe, text="Graph Outliers", command=lambda: graph_outliers(csv, clicked1.get(),
                                                                             clicked2.get(), order.get()))
    outlierbutton.pack(side=BOTTOM)
    Strucbutton1 = Radiobutton(buttonframe, text="Linear Approximation", variable=order, value=1)
    Strucbutton1.pack()
    Strucbutton2 = Radiobutton(buttonframe, text="Quadratic Approximation", variable=order, value=2)
    Strucbutton2.pack()
    loggraph = Radiobutton(buttonframe, text="Logarithmic Approximation", variable=order, value=999)
    loggraph.pack()

# clears the frame when a new file is opened. called only after the first file is opened
# as options need to be updated with each new file.
def undraw():
    windowframe.pack_forget()
    buttonframe.pack_forget()


# builds a window, canvas within the window, and calls
# create_figure() with relevant parameters to populate canvas.
def graph(file, xval, yval, limit, robust, order):
    global canvas
    graphwindow = Toplevel(height=900, width=1000)
    if order > 500:
        log=True
        order = 1
    else:
        log=False
    fig = create_figure(file, xval, yval, robust, order, log)
    if limit != 0:
        plt.axhline(y=(limit / 1000), color='r', linestyle='-')
    canvas = FigureCanvasTkAgg(fig, master=graphwindow)
    canvas.draw()
    canvas.get_tk_widget().pack()
    button = tk.Button(graphwindow, text="Close", command=graphwindow.destroy)
    button.pack()


# creates a figure containing the graph, type figure
def create_figure(file, xaxis, yaxis, robust, order, log):
    f, dummy = plt.subplots(figsize=(6, 6))
    sns.regplot(x=xaxis, y=yaxis, data=file, robust=robust, order=order, logx=log, ci=68)
    return f

def graph_outliers(file, xaxis, yaxis, order):
    graphwindow = Toplevel(height=900, width=1000)
    if order > 500:
        order = 1

    fig = outlier_figure(file, xaxis, yaxis, order)
    canvas = FigureCanvasTkAgg(fig, master=graphwindow)
    canvas.draw()
    canvas.get_tk_widget().pack()
    button = tk.Button(graphwindow, text="Close", command=graphwindow.destroy)
    button.pack()


def outlier_figure(file, xaxis, yaxis, order):
    f, dummy = plt.subplots(figsize=(6, 6))
    sns.residplot(x=xaxis, y=yaxis, data=file, lowess=True, order=order)
    return f


# Main begins here
# plt.pyplot.ion() for interactive mode, may want to investigate
firstRun = True
root = tk.Tk()
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
