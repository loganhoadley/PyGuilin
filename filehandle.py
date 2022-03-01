import pandas as pd
from datetime import datetime
# determines if the file is formatted in wide format or not,
# ie did it come from pi vision or was it hand-made

def filedetermine(file):
    print(file.columns[0])
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


    print(file.loc[i, 'Time'])
    file=file.groupby(file.index).sum()
    print(file)
    #df2 = file.pivot(index='Time', columns='Data Source', values='Value')
    #print(df2)
