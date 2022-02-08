# matplotlib.pyplot.ion() enables interactive mode, which should serve the final product
from tkinter import filedialog
import tkinter as tk
import csv
# import seaborn as sns
# import matplotlib as plt

from tkinter import *

headerlist = ["sample"]
data = []


def openfile():
    filepath = filedialog.askopenfilename(initialdir="%USERPROFILE%/Downloads",
                                          filetypes=(("Comma Separated Value Lists", "*.csv"), ("All Files", "*.*")))
    with open(filepath, newline='') as csvfile:
        data = []
        header = csvfile.readline()
        headerlist = header.split(',')
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    print(headerlist)  # prints headerlist as it exists when created from .csv
    print(data[1][0])  # 2nd column timestamp for debug purposes


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

drop = OptionMenu(root, clicked, headerlist)
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
