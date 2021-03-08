from pathlib import *
import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('amount_of_experiments', help='How many experiments you need', type=int)
parser.add_argument('amount_of_bases', help='How many bases ou need for distribution generators', type=int)
parser.add_argument('path_to_main_script', help="Path to the whole script with a removed line of RMULT")

args = parser.parse_args()

amount_of_experiments = args.amount_of_experiments
amount_of_bases = args.amount_of_bases
path_to_main_script = args.path_to_main_script

print("""experiments: {}, bases: {}, main_script {}""".format(amount_of_experiments, amount_of_bases, path_to_main_script))

if amount_of_bases <= 0 or amount_of_experiments <= 0:
    print("0 or less amount was given")
    raise argparse.ArgumentError() 

template = "RMULT "
folder = "./gpss_experiment_scripts/"
folder_path = Path(folder)
if folder_path.exists():
    for i in folder_path.iterdir():
        i.unlink()
    folder_path.rmdir()
print("new folder created")
folder_path.mkdir()
main_script = Path(path_to_main_script)

if not main_script.exists():
    print ("main script does not exist")
    raise argparse.ArgumentError()

main_script_lines = []

with main_script.open('r') as file:
    main_script_lines = file.readlines()

for exp in range(amount_of_experiments):
    filled_template = str(template)
    a = np.round(np.random.rand(amount_of_bases) * 10000000, 0)

    for index, i in enumerate(a):
        filled_template = filled_template + str(int(i))
        if index != amount_of_bases - 1:
            filled_template += ","
        else:
            filled_template += "\n"
    new_file = [filled_template]
    new_file.extend(main_script_lines)
    new_file_path = Path(folder).joinpath(f"{exp}.txt")
    new_file_path.touch()
    with new_file_path.open('w') as file:
        file.writelines(new_file)

