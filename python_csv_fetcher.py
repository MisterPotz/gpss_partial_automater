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
generated_files_list = []

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

raw_report_name = "raw_report.csv"
data.to_csv(raw_report_name, index=False, sep=",")
generated_files_list.append(raw_report_name)

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
means_and_disps_name = "means_and_disps.csv"
means_disps.to_csv(means_and_disps_name, sep=",", index=True)

generated_files_list.append(means_and_disps_name)

# confidence tables
conf = pd.read_csv("confidence_interval.csv", index_col=0)

def find_t(confidence_table, N, accuracy):
    acc = accuracy / 2
    v = N - 1
    t = confidence_table.loc[ confidence_table.index == v, confidence_table.columns.astype('float64') == acc ].to_numpy()[0][0]
    return t

import math
def confidence_interval(accuracy, arr):
    mean, disp = mean_disp(arr)
    t = find_t(conf, arr.shape[0], accuracy)
    diff = t * math.sqrt(disp / arr.shape[0])
    return (mean, diff)

def prettify_confidence_interval(mean, disp):
    return f"{mean} +- {disp}"

print(conf.columns)
for i in raw_columns:
    framei = pd.DataFrame(columns=["N = 5", "N = 20"])
    columns = framei.columns
    def create_row(column, accuracy):
        arr = raw_data[column]
        row = []
        for i in [5, 20]:
            teta = confidence_interval(accuracy, arr[:i])
            teta = prettify_confidence_interval(teta[0], teta[1])
            row.append(teta)
        row = dict(zip(columns, row))
        return row

    for acc in (0.1, 0.05):
        row = create_row(i, acc)
        framei = framei.append(row, ignore_index=True)

    framei.index = ['acc 0.1', 'acc 0.05']
    framei_name = f"stanok_conf_{i}.csv"
    framei.to_csv(framei_name, sep=',', index=True)
    generated_files_list.append(framei_name)

print(f"output files : {generated_files_list}")