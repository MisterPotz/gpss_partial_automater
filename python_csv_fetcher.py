from pathlib import Path, PurePosixPath
import sys
import re
import pandas as pd
from pandas.core.frame import DataFrame
import argparse

# CONSTS 
first_n = 5
second_n = 20

parser = argparse.ArgumentParser()

parser.add_argument('path', help='Path to the GPSS reports folders')
parser.add_argument('--target_column_index', dest="target_column_index", help='Index of statistics target column (UTILIZATION by default is 2)', type=int, default=2)
parser.add_argument("--n_sizes", dest="n_sizes", help="Sizes of dataset, by default is '5 20'", type=str, default="5 20")

args = parser.parse_args()

path = args.path
target_column_index = args.target_column_index
n_sizes = args.n_sizes.split()
first_n = int(n_sizes[0])
second_n = int(n_sizes[1])

reports_folder = Path(path)

print(reports_folder.name)

# must format the output folder
for i in reports_folder.iterdir():
    # remove unnecessary data from file if possible
    lines = []
    with i.open('r') as file:
        lines = file.readlines()
    slice_index1 = -1
    slice_index2 = -1
    pattern_name_value_block = re.compile(r".*(NAME).*(VALUE).*")
    pattern_facility_block = re.compile(r".*(FACILITY).*")
    pattern_header = re.compile(r".*(GPSS World Simulation Report).*")

    for index, line in enumerate(lines):
        if re.match(pattern_name_value_block, line.strip()) is not None:
            print("matched name value block ", line)
            slice_index1 = index
            continue
        if re.match(pattern_facility_block, line.strip()) is not None:
            print("matched facility block", line)
            slice_index2 = index

    if slice_index1 > -1:
        lines = lines[:slice_index1] + lines[slice_index2:]  
    indices_to_filter = list()
    for index, line in enumerate(lines):
        if re.match(pattern_header, line.strip()) is not None:
            indices_to_filter.extend(list(range(index, index + 4)))
    lines = list(filter(lambda x: x[0] not in indices_to_filter, enumerate(lines)))
    lines = list(map(lambda x: x[1], lines))

    if re.fullmatch(r".*(RMULT).*", lines[0].strip()) is None:
        print("no RMULT found")
        order_index = i.name
        gpss_generated=Path("./gpss_experiment_scripts/")
        related_file_with_mult = gpss_generated.joinpath(f"{order_index}")
        first_line = None
        with related_file_with_mult.open('r') as file:
            lines1 = file.readlines()
            first_line = lines1[0]
        lines.insert(0, first_line)

    # on the end of the file there are bad symbols
    pattern_queue_entity =re.compile(r"[\s]*[A-Z0-9_]+[\s]+[0-9]+[\s]+[0-9]+.*")

    queue_last = len(lines)
    for index, line in enumerate(lines[::-1]):
        if re.fullmatch(pattern_queue_entity, line.strip()) is not None:
            print(line)
            queue_last = -index
            break
    if (queue_last < 0):
        lines = lines[:queue_last]
    
    with i.open('w') as file:
        file.writelines(lines)


# recreate the folder if necessary
data = pd.DataFrame()
output_folder = Path("./output/")
if output_folder.exists() and output_folder.is_dir():
    for i in output_folder.iterdir():
        i.unlink()
    output_folder.rmdir()
output_folder.mkdir()


# create the raw data for all found stanoks
for index, i in enumerate(reports_folder.iterdir()):
    with open(i, 'r') as report:
        print(f"reading file {i.name}")
        lines = list(map(lambda x: x.strip().replace("\n", ""), report.readlines()))
        lines = list(filter(lambda x: re.match(r"^[\ ]*(STANOK|MACHINE)[0-9]*[\ ]+", x), lines))
        def name_util(x: str):
            split = x.split()
            return (split[0], split[target_column_index])
        stanoks_utils = dict(map(name_util, lines))
        print(stanoks_utils)
        # fill the data frame
        data = data.append(stanoks_utils, ignore_index=True)

print(data)

# save as rawa report
raw_report_name = "raw_report.csv"
raw_report_path = output_folder.joinpath(raw_report_name)
with raw_report_path.open('w') as file:
    data.to_csv(file, index=False, sep=",")

import numpy as np

# analyze means and dispersion 
def mean_disp(arr: np.array):
    mean = arr.mean()
    disp =  (arr - mean) ** 2
    disp = np.sum(disp) / ( arr.shape[0] - 1)
    return (mean, disp)

raw_data = None
with raw_report_path.open('r') as file:
    raw_data = pd.read_csv(file, sep=',')
raw_columns=raw_data.columns
means_disps = \
    pd.DataFrame(columns=[f"Оценка мат. ожидания N = {first_n}", 
    f"Оценка дисперсии N = {first_n}", f"Оценка мат. ожидания N = {second_n}", f"Оценка дисперсии N = {second_n}"])

for i in raw_columns:
    arr = raw_data[i]
    row = []
    for g in (first_n, second_n):
        arrg = arr[:g]
        meang, dispg = mean_disp(arrg)
        row.extend((meang, dispg))
    print(f"row for stanok {i} : {row}")
    means_disps = means_disps.append(dict(zip(means_disps.columns, row)), ignore_index = True)
means_disps.index = raw_columns
means_and_disps_name = "means_and_disps.csv"
means_path=output_folder.joinpath(means_and_disps_name)
with means_path.open('w') as file:
    means_disps.to_csv(file, index=True, sep=",")

# confidence table
conf = pd.read_csv("confidence_interval.csv", index_col=0)

def find_t(confidence_table, N, accuracy):
    acc = accuracy / 2
    v = N - 1
    if v == 0:
        raise argparse.ArgumentError(None, f"size of the given dataset if too small {v}")
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

# find confidence interval for our data
for i in raw_columns:
    framei = pd.DataFrame(columns=[f"N = {first_n}", f"N = {second_n}"])
    columns = framei.columns
    def create_row(column, accuracy):
        arr = raw_data[column]
        row = []
        for i in [first_n, second_n]:
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
    framei_path = output_folder.joinpath(framei_name)
    with framei_path.open('w') as file:
        framei.to_csv(file, sep=',', index=True)

# show newly created files
print(f"output files : {list(output_folder.iterdir())}")