# matplotlib.pyplot.ion() enables interactive mode, which should serve the final product
from tkinter import filedialog
import tkinter as tk
import csv
import seaborn as sns
import numpy as np
import pandas as pd

import matplotlib as plt

sns.set_theme(color_codes=True)

from tkinter import *

headerlist = ["sample",
              "sample2",
              "sample 3"]
data = []


def openfile():
    filepath = filedialog.askopenfilename(initialdir="%USERPROFILE%/Downloads",
                                          filetypes=(("Comma Separated Value Lists", "*.csv"), ("All Files", "*.*")))
    csv = pd.read_csv(filepath)
    #with open(filepath, newline='') as csvfile:
    #    data = []
    #    header = csvfile.readline()
    #    headerlist = header.split(',')
    #    data.append(header)
    #    reader = csv.reader(csvfile)
    #    for row in reader:
    #        data.append(row)
    count = 0
    headers = list(csv.columns)

    for col_name in csv.columns:
        count=count+1
        print(count, "--", col_name)
        #headers.append(col_name)

    #for n in headerlist:
    #    count = count + 1
    #    print(count, "--", n)  # prints headerlist as it exists when created from .csv

    arg1 = input("Select argument 1: ")
    arg2 = input("Select argument 2: ")
    arg1 = int(arg1)
    arg2 = int(arg2)

    arg1title = headers[arg1-1]
    arg2title = headers[arg2-1]
    print(arg1title)
    print(arg2title)
    #dataset = np.array(data)
    #print(dataset)
    sns.displot(csv, x=arg1title, y=arg2title)
    plt.pyplot.show()


# maybe just build a window in this open function that contains the graph,
# having the options for selection show up in the new window
# have the main window maybe contain some documentation and guiding the user? I'm not sure exactly how to get tkinter
# to behave in the way I want, I'll play around with the order


root = tk.Tk()
root.title("PyGuilin Dev Build")


def show():
    label.config(text=clicked.get())


clicked = StringVar()
clicked.set("Parameter 1")

drop = OptionMenu(root, clicked, *headerlist)
drop.pack()

main_menu = tk.Menu(root)

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
