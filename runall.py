# runall.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 21 Jun 2023

import os
import subprocess
from roundup_scripts.data_compare import compare_new_data #User-defined

print(os.getcwd())

# Path to venv python
venv_python_path = "/Users/dr.work/Dropbox/Code_Dropbox/Brookings/lorae_roundup/roundup/proj_env/bin/python"

# Make a list of roundup_scripts used in the scraper.
roundup_scripts = ["BOE", "Chicago", "NBER"]
scraper_paths = [f"roundup_scripts/scrapers/{script}.py" for script in roundup_scripts]

# Progress bar 
total_tasks = len(scraper_paths)
for i, scraper in enumerate(scraper_paths, start=1):
    subprocess.call([venv_python_path, scraper])
    print(f"-----\n({i}/{total_tasks}) tasks done\n-----")

# Comparing data
print("Comparing data")
historic_paths = [f"historic_data/{script}.json" for script in roundup_scripts]
processed_paths = [f"processed_data/{script}.json" for script in roundup_scripts]

# note to self: add error if historic paths length does not equal processed
# paths length
for i, script in enumerate(roundup_scripts, start=0):
    print(f"{script}")
    compare_new_data(historic_paths[i], processed_paths[i])
    print(f"Compared data for {script}")

print("done.")

'''
subprocess.call([venv_python_path, "roundup_scripts/scrapers/BOE.py"])
subprocess.call([venv_python_path, "roundup_scripts/scrapers/Chicago.py"])
subprocess.call([venv_python_path, "roundup_scripts/scrapers/NBER.py"])
'''

