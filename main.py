# matplotlib.pyplot.ion() enables interactive mode, which should serve the final product
from tkinter import filedialog
import tkinter as tk
import csv
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib as plt
from functools import partial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sns.set_theme(color_codes=True)

from tkinter import *

headerlist = ["sample" ]
data = []
plt.pyplot.ion()


def graph(file, arg1, arg2):
    sns.displot(file, x=arg1, y=arg2)
    plt.pyplot.show()
      #graph =
      #graphic = FigureCanvasTkAgg(graph, graphwindow)
      #graphic.get_tk_widget().pack(side=LEFT, fill=BOTH)

def openfile():
    filepath = filedialog.askopenfilename(initialdir="%USERPROFILE%/Downloads",
                                          filetypes=(("Comma Separated Value Lists", "*.csv"), ("All Files", "*.*")))
    csv = pd.read_csv(filepath)
    headers = list(csv.columns)

    graphwindow=Toplevel(root)
    graphwindow.geometry("500x400")
    graphwindow.title(filepath)
    buttonframe = Frame(graphwindow)
    buttonframe.pack(side=LEFT)
    clicked1 = StringVar()
    clicked1.set("Parameter 1")
    clicked2 = StringVar()
    clicked2.set("Parameter 2")
    windowframe = Frame(graphwindow)
    windowframe.pack(side=RIGHT)
    drop1 = OptionMenu(buttonframe, clicked1, *headers)
    drop1.pack(side=BOTTOM)
    drop2 = OptionMenu(buttonframe, clicked2, *headers)
    drop2.pack(side=BOTTOM)

    graphbutton = Button(buttonframe, text= "Generate", command = lambda: graph(csv, clicked1.get(), clicked2.get()))
    graphbutton.pack(side=BOTTOM)

    #  sns.displot(csv, x=clicked1, y=clicked2)
    #  plt.pyplot.show()


# maybe just build a window in this open function that contains the graph,
# having the options for selection show up in the new window
# have the main window maybe contain some documentation and guiding the user? I'm not sure exactly how to get tkinter
# to behave in the way I want, I'll play around with the order


root = tk.Tk()
root.title("PyGuilin Dev Build")
main_menu = tk.Menu(root)
root.geometry("350x200")
root.config(menu=main_menu)
file_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=openfile)
file_menu.add_command(label="Export as...")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

label = Label(root, text=" ")
label.pack()

root.mainloop()


