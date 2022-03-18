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

        sourcename = str(file.loc[i, 'Data Source'])
        sourcetime = str(file.loc[i, 'Time'])
        file.loc[i, 'Data Source'] = sourcename.rpartition('\\')[-1]
        # file.loc[i,'Data Source']=sourcename.removeprefix
        # ("\\\\TUSSITCDIIPIAF\TUS_TC_PROD_v7\_PRIMARY_L1_EQUIPMENT\GUILIN_04\\")
        # this is an unbelievably stupid way of correcting the time but it's what my little gremlin brain came up with
        file.loc[i, 'Time'] = '-'.join(sourcetime.rpartition('.')[0:-2])
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

    # print(file.loc[i, 'Time'])
    # file = file.groupby(file.index).sum()
    # print(file)
    # df2 = file.pivot(index='Time', columns='Data Source', values='Value')
    # print(df2)


def long_to_wide(input_file):
    """
    This function takes a longform factory provided CSV file and converts into a wide-form dictionary.
    Values are sorted under timestamps at each second.
    Gaps between seconds are filled in, as these gaps are caused by the machine's storage saving algorithm, where it is
    presumed that the sensors are not detecting perceptible changes in the reading.
    This dictionary is structured to be interpreted as a CSV table.
    :param input_file: The name of the csv file, as a string.
    :return: A wide-form table stored in a dictionary.
    """
    # Dictionary to store csv data in
    wide_data = {}
    # List to store all the data sources for headers
    sources = ['Time']
    with open(input_file, encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row['Time'] != '':
                # The timestamps are stored in ISO format down to millisecond precision.
                # Unfortunately, the milliseconds are often truncated such that Python does not recognize the stamp.
                # This appends zeroes to the timestamp until it is recognized by Python.
                try:
                    time_stamp = datetime.fromisoformat(row['Time'])
                    time_stamp = time_stamp.isoformat(sep=' ', timespec='seconds')
                except ValueError:
                    time_stamp = correctTimestamp(row['Time'])
                # Collecting the datasource and the value, and formatting the datasource appropriately.
                source = row['Data Source']
                value = row['Value']
                source = source.rpartition('\\')[-1]
                # If the source is not in the sources list, append it.
                if source not in sources:
                    sources.append(source)
                # If the timestamp isn't in the dictionary yet, insert it as a new key.
                if time_stamp not in wide_data:
                    wide_data[time_stamp] = {'Time': time_stamp, source: value}
                else:
                    # If it exists already, update the value of the source in this row.
                    wide_data[time_stamp][source] = value
    with open('test.csv', 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=sources)
        # Headers are defined at the beginning of the script.
        writer.writeheader()
        # Dictionary of last known values, for filling in the gaps in the data.
        # Initialized to blank spaces.
        last_known_values = {}
        for s in sources:
            last_known_values[s] = ''
        # Traverse the values in chronological order
        for key in sorted(wide_data.keys()):
            # For each header, check if a value exists at that location, if not, then set it to last known value.
            for s in sources:
                if s not in wide_data[key] or wide_data[key][s] == '':
                    wide_data[key][s] = last_known_values[s]
                # If value exists at this location, update last known value.
                else:
                    last_known_values[s] = wide_data[key][s]
    return wide_data
