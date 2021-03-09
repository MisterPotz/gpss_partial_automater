from pathlib import Path, PurePosixPath
import re
from pandas.core.frame import DataFrame
import argparse

# CONSTS 
first_n = 5
second_n = 20

parser = argparse.ArgumentParser()

parser.add_argument('report_file', help='Path to the report file to split')
parser.add_argument('reports_folder', help='Path to folder to store report files')

args = parser.parse_args()

report_file = Path(args.report_file)
reports_folder = Path(args.reports_folder)
print(reports_folder.name)

if reports_folder.exists() and reports_folder.is_dir():
    for i in reports_folder.iterdir():
        i.unlink()
    reports_folder.rmdir()
reports_folder.mkdir()

lines = []
with report_file.open('r') as file:
    lines = file.readlines()

file_counter = 1
split_pattern = re.compile(r".*<>\?.*")
current_file_lines = []

for index, i in enumerate(lines):
    if re.match(split_pattern, i) is not None:
        new_file_path = reports_folder.joinpath(f"{file_counter}.txt")
        file_counter += 1
        with new_file_path.open('w') as file:
            file.writelines(current_file_lines)
        current_file_lines = []
    else:
        current_file_lines.append(i)

if len(current_file_lines) > 0:
    new_file_path = reports_folder.joinpath(f"{file_counter}.txt")
    with new_file_path.open('w') as file:
        file.writelines(current_file_lines)
    current_file_lines = []