# runall.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 27 Jul 2023

import os
import subprocess
import pandas as pd
from roundup_scripts.compare import compare_historic # User-defined

# Here, we import all the scripts from roundup_scripts/scrapers
import sys
sys.path.append('roundup_scripts/scrapers')
import BEA
import BFI
import BIS
import BOE
import ECB
import Fed_Atlanta
import Fed_Board
import Fed_Chicago
import Fed_NewYork
import IMF
import NBER

print(os.getcwd())

# Path to venv python
venv_python_path = "venv/Scripts/python.exe"
#venv_python_path = "/Users/dr.work/Dropbox/Code_Dropbox/Brookings/lorae_roundup/roundup/proj_env/bin/python"

# Make a dictionary of roundup_scripts used in the scraper.

roundup_scripts = {
    "BEA": BEA, 
    "BFI": BFI,
    "BIS": BIS,
    "BOE": BOE, 
    "ECB": ECB, 
    "Fed_Atlanta": Fed_Atlanta,
    "Fed_Board": Fed_Board,
    "Fed_Chicago": Fed_Chicago, 
    "Fed_NewYork": Fed_NewYork,
    "IMF": IMF, 
    "NBER": NBER
}

# Part 1: Scraping Data
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
print(f"--------------------\n Part 2: Comparing to Historical Data \n--------------------")

# Calling the compare function from historic/compare.py
compare_historic(df)
print("compare.py complete.")

print(f"--------------------\n Script has completed running. \n--------------------")

