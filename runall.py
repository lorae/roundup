# runall.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 21 Jun 2023

import os
import subprocess
import pandas as pd
from roundup_scripts.data_compare import compare_new_data #User-defined
from roundup_scripts.compare import compare_historic # User-defined

# Here, we import all the scripts from roundup_scripts/scrapers
import sys
sys.path.append('roundup_scripts/scrapers')
import BOE
import Chicago
import NBER


print(os.getcwd())

# Path to venv python
venv_python_path = "C:/Users/LStojanovic/Downloads/roundup/venv/Scripts/python.exe" #maybe?
#venv_python_path = "/Users/dr.work/Dropbox/Code_Dropbox/Brookings/lorae_roundup/roundup/proj_env/bin/python"

# Make a dictionary of roundup_scripts used in the scraper.
roundup_scripts = {"BOE": BOE, "Chicago": Chicago, "NBER": NBER}
#scraper_paths = [f"roundup_scripts/scrapers/{script}.py" for script in roundup_scripts]

# Part 1: Scraping Data
# print a message that data is being scraped
print(f"--------------------\n Part 1: Data Scrape \n--------------------")

# Initialize an empty list to hold all data frames
dfs = []

# Progress bar 
total_tasks = len(roundup_scripts)
for i, (name, scraper) in enumerate(roundup_scripts.items(), start=0):
    # Append the result of each scrape to the list
    dfs.append(scraper.scrape())
    print(f"-----\n Data Scrape: ({i+1}/{total_tasks}) tasks done\n-----")

# Concatenate all data frames in the list into a single data frame
df = pd.concat(dfs, ignore_index=False)

# Part 2: Comparing to historical data
# print a message that data is being compared to historical
print(f"--------------------\n Part 2: Comparing to Historical Data \n--------------------")


historic_paths = [f"historic_data/{script}.json" for script in roundup_scripts]
processed_paths = [f"processed_data/{script}.json" for script in roundup_scripts]
new_paths = [f"new_data/{script}.json" for script in roundup_scripts]

# now we're trying a new thing
compare_historic(df)

# note to self: add error if historic paths length does not equal processed
# paths length. They should be the same because for each source (e.g. BOE, NBER),
# there should be one historic data file and one processed data file.
'''
for i, script in enumerate(roundup_scripts, start=0):
    print(f"{script}")
    compare_new_data(historic_paths[i], processed_paths[i], new_paths[i])
    print(f"Compared data for {script}")
'''

print(f"--------------------\n Script has completed running. \n--------------------")

'''
subprocess.call([venv_python_path, "roundup_scripts/scrapers/BOE.py"])
subprocess.call([venv_python_path, "roundup_scripts/scrapers/Chicago.py"])
subprocess.call([venv_python_path, "roundup_scripts/scrapers/NBER.py"])
'''

