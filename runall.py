# runall.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 21 Jun 2023

import os
import subprocess
from scripts.data_compare import compare_new_data #User-defined

print(os.getcwd())

# Path to venv python
venv_python_path = "C:/Users/LStojanovic/Downloads/roundup/venv/Scripts/python.exe"

# Make a list of scripts used in the scraper.
scripts = ["BOE", "Chicago", "NBER"]
scraper_paths = [f"scripts/scrapers/{script}.py" for script in scripts]

# Progress bar 
total_tasks = len(scraper_paths)
for i, scraper in enumerate(scraper_paths, start=1):
    subprocess.call([venv_python_path, scraper])
    print(f"-----\n({i}/{total_tasks}) tasks done\n-----")

# Comparing data
print("Comparing data")
historic_paths = [f"historic_data/{script}.json" for script in scripts]
processed_paths = [f"processed_data/{script}.json" for script in scripts]

# note to self: add error if historic paths length does not equal processed
# paths length
for i, script in enumerate(scripts, start=1):
    compare_new_data(historic_paths[i], processed_paths[i])
    print("Compared data for {script}")

print("done.")

'''
subprocess.call([venv_python_path, "scripts/scrapers/BOE.py"])
subprocess.call([venv_python_path, "scripts/scrapers/Chicago.py"])
subprocess.call([venv_python_path, "scripts/scrapers/NBER.py"])
'''

