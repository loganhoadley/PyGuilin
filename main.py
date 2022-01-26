# matplotlib.pyplot.ion() enables interactive mode, which should serve the final product


# import seaborn as sns
# import matplotlib as plt
import tkinter as tk
from tkinter import filedialog
import csv

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
# data[] should contain a 2D array, which contains elements as lists with data associations from the .CSV
data = []

with open(file_path, newline='') as csvfile:
    header = csvfile.readline()
    headerList = header.split(',')
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row)
# data is now loaded

# print(headerList)
print(headerList[4])
print(data[1][0])
# access in 2d array, 1st element is the row of the CSV, 2nd element is
# the index of the precise entry, or use one element for the whole row

