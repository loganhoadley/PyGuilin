# matplotlib.pyplot.ion() enables interactive mode, which should serve the final product
# import seaborn as sns
# import matplotlib as plt

import tkinter as tk
import csv
from tkinter import filedialog


def openfile():
    filepath = filedialog.askopenfilename(initialdir="%USERPROFILE%/Downloads",
                                          filetypes=(("Comma Separated Value Lists", "*.csv"), ("All Files", "*.*")))

    with open(filepath, newline='') as csvfile:
        header = csvfile.readline()
        headerlist = header.split(',')
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)

    print(headerlist)
    print(headerlist[4])
    print(data[1][0])


data = []

root = tk.Tk()
root.title("PyGuilin Dev Build")

main_menu = tk.Menu(root)
root.config(menu=main_menu)
file_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=openfile)
file_menu.add_command(label="Export as...")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)


root.mainloop()


# root = tk.Tk()
# root.withdraw()

# data[] should contain a 2D array, which contains elements as lists with data associations from the .CSV
#

# data is now loaded


# access in 2d array, 1st element is the row of the CSV, 2nd element is
# the index of the precise entry, or use one element for the whole row
