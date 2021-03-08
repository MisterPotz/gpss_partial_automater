from pathlib import Path, PurePosixPath
import sys
import re
import pandas as pd
from pandas.core.frame import DataFrame

path = sys.argv[1]
target_column_index = int(sys.argv[2])

reports_folder = Path(path)

print(reports_folder.name)

print([x for x in reports_folder.iterdir()])

data = pd.DataFrame()

for index, i in enumerate(reports_folder.iterdir()):
    with open(i, 'r') as report:
        print(f"reading file {i.name}")
        lines = list(map(lambda x: x.strip().replace("\n", ""), report.readlines()))
        lines = list(filter(lambda x: re.match(r"^[\ ]*(STANOK)[0-9]*[\ ]+", x), lines))
        def name_util(x: str):
            split = x.split()
            return (split[0], split[target_column_index])
        stanoks_utils = dict(map(name_util, lines))
        print(stanoks_utils)
        # fill the data frame
        data = data.append(stanoks_utils, ignore_index=True)

print(data)

data.to_csv("raw_report.csv", index=False, sep=",")

import numpy as np

def mean_disp(arr: np.array):
    mean = arr.mean()
    disp =  (arr - mean) ** 2
    disp = np.sum(disp) / ( arr.shape[0] - 1)
    return (mean, disp)

raw_data = pd.read_csv("raw_report.csv", sep=',')
raw_columns=raw_data.columns
means_disps = \
    pd.DataFrame(columns=["Оценка мат. ожидания N = 5", 
    "Оценка дисперсии N = 5", "Оценка мат. ожидания N = 20", "Оценка дисперсии N = 20"])

for i in raw_columns:
    arr = raw_data[i]
    row = []
    for g in (5, 20):
        arrg = arr[:g]
        meang, dispg = mean_disp(arrg)
        row.extend((meang, dispg))
    print(f"row for stanok {i} : {row}")
    means_disps = means_disps.append(dict(zip(means_disps.columns, row)), ignore_index = True)
means_disps.index = raw_columns
means_disps.to_csv("means_and_disps.csv", sep=",", index=True)

# confidence tables
conf = pd.read_csv("confidence_interval.csv", index_col=0)

def find_t(confidence_table, N, accuracy):
    acc = accuracy / 2
    v = N - 1
    return confidence_table.loc[ confidence_table.index == v, confidence_table.columns.astype('float64') == acc ]

def confidence_interval(accuracy, arr):
    mean, disp = mean_disp(arr)
    t = find_t(conf, arr.shape[0], accuracy)
    diff = t * sqrt(disp / arr.shape[0])
    return (mean, diff)

for i in raw_columns:
    framei = pd.DataFrame(columns=["N = 5", "N = 20"])
    columns = framei.columns
    new_row = []
    tetas = list(map(lambda x: confidence_interval(accuracy=), zip([])))
    framei.append()
    for accs in [0.1, 0.05]:
        
    