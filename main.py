#testing Seaborn library and its interaction in pycharm
#show() needs to be called in order to explicitly draw the generated plot in the IDE
#matplotlib.pyplot.ion() enables interactive mode, which should serve the final product

#import seaborn as sns
#import matplotlib as plt
import tkinter as tk
from tkinter import filedialog
import csv

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

with open(file_path, newline='') as csvfile:
    header = csvfile.readline()
    print(header)
    headerlist = header.split(',')
    reader= csv.reader(csvfile)
    for row in reader:
        print(', '.join(row))

print(headerlist)
print(len(headerlist))
print(headerlist[4])

