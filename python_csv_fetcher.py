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