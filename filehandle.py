import pandas as pd
from datetime import datetime
import csv
# determines if the file is formatted in wide format or not,
# ie did it come from pi vision or was it hand-made

def filedetermine(file):
    if file.columns[0] == "Data Source":
        return False
    else:
        return True


def correctTimestamp(timestamp):
        try:
            correctedtimestamp = timestamp + "0"
            sourcestamp = datetime.fromisoformat(correctedtimestamp)
            return sourcestamp.isoformat(sep=' ', timespec='seconds')
        except ValueError:
            bufferedTimestamp = timestamp + "0"
            return correctTimestamp(bufferedTimestamp)


def filecorrect(file):
    # iterates downloaded data from OSI and removes the unnecessary tags for the file location from the processing
    for i in file.index:

        sourcename=str(file.loc[i,'Data Source'])
        sourcetime=str(file.loc[i,'Time'])
        file.loc[i,'Data Source']=sourcename.rpartition('\\')[-1]
        # file.loc[i,'Data Source']=sourcename.removeprefix
        # ("\\\\TUSSITCDIIPIAF\TUS_TC_PROD_v7\_PRIMARY_L1_EQUIPMENT\GUILIN_04\\")
        # this is an unbelievably stupid way of correcting the time but it's what my little gremlin brain came up with
        file.loc[i,'Time'] = '-'.join(sourcetime.rpartition('.')[0:-2])
        if file.loc[i, 'Time'] != '':
            try:
                sourcestamp = datetime.fromisoformat(file.loc[i, 'Time'])
                file.loc[i, 'Time'] = sourcestamp.isoformat(sep=' ', timespec='seconds')
            except ValueError:
                file.loc[i, 'Time'] = correctTimestamp(file.loc[i, 'Time'])
    print("header:")
    print(file.columns)
    print("data at index 0")
    print(file.loc[1])

    #print(file.loc[i, 'Time'])
    #file = file.groupby(file.index).sum()
    #print(file)
    #df2 = file.pivot(index='Time', columns='Data Source', values='Value')
    #print(df2)

def LongToWide(input_file):
    # Dictionary to store csv data in
    wide_data = {}
    # List to store all the data sources for headers
    sources = ['Time']
    with open(input_file, encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row['Time'] != '':
                try:
                    time_stamp = datetime.fromisoformat(row['Time'])
                    time_stamp = time_stamp.isoformat(sep=' ', timespec='seconds')
                except ValueError:
                    time_stamp = correctTimestamp(row['Time'])
                source = row['Data Source']
                value = row['Value']
                source = source.rpartition('\\')[-1]
                if source not in sources:
                    sources.append(source)
                if time_stamp not in wide_data:
                    wide_data[time_stamp] = {'Time': time_stamp, source: value}
                else:
                    wide_data[time_stamp][source] = value
    with open('test.csv', 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=sources)
        # Headers are defined at the beginning of the script.
        writer.writeheader()
        # This takes each dictionary entry, which is itself a dictionary, and writes the values to the CSV file.
        for key in wide_data:
            writer.writerow(wide_data[key])

LongToWide("Extruder_Temp.csv")
