# matplotlib.pyplot.ion() enables interactive mode, which should serve the final product
from tkinter import filedialog
import tkinter as tk
import seaborn as sns
import pandas as pd
import matplotlib as plt
from tkinter import *
sns.set_theme(color_codes=True)

headerlist = ["sample"]
data = []
plt.pyplot.ion()
global csv
firstRun = True

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
    sliderlabel = Label(buttonframe, text="Width deviation limit in\n hundredths of millimeters: ")
    sliderlabel.pack(side=TOP)
    slider = Scale(buttonframe, from_=0, to=500, orient=HORIZONTAL)
    slider.pack(side=TOP)
    graphbutton = Button(buttonframe, text="Generate", command=lambda: graph(csv, clicked1.get(), clicked2.get()))
    graphbutton.pack(side=BOTTOM)


def undraw():
    windowframe.pack_forget()
    buttonframe.pack_forget()



def graph(file, arg1, arg2):
    sns.regplot(x=arg1, y=arg2, data=file)
    plt.pyplot.show()
    #  need this method to be superseded
    #  graph =
    #  graphic = FigureCanvasTkAgg(graph, graphwindow)
    #  graphic.get_tk_widget().pack(side=LEFT, fill=BOTH)


def openfile():
    global filepath, headers, firstRun, csv
    filepath = filedialog.askopenfilename(initialdir="%USERPROFILE%/Downloads",
                                          filetypes=(("Comma Separated Value Lists", "*.csv"), ("All Files", "*.*")))
    csv = pd.read_csv(filepath)
    headers = list(csv.columns)
    if firstRun:
        startLabel.pack_forget()
        firstRun=False
    else:
        undraw()
    draw()

root = tk.Tk()
root.title("PyGuilin Dev Build")
main_menu = tk.Menu(root)
root.geometry("500x800")
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
