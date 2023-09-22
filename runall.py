# runall.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 8 Sept 2023

import os
import subprocess
import pandas as pd
from roundup_scripts.compare import compare_historic # User-defined
# Here, we import all the scripts from roundup_scripts/scrapers
from roundup_scripts.scrapers import *

# Function to read script status from file
def read_scraper_status(filename):
    scraper_status = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                name, status = line.strip().split(',')
                scraper_status[name] = status
    except FileNotFoundError:
        # If file not found, initialize all scripts to "on"
        scraper_status = {name: "on" for name in roundup_scripts.keys()}
    return scraper_status

# Function to write script status to file
def write_scraper_status(filename, scraper_status):
    with open(filename, 'w') as f:
        for name, status in scraper_status.items():
            f.write(f"{name},{status}\n")

# Initialize scraper_status from file
scraper_status = read_scraper_status("scraper_status.txt")

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
    "Fed_Board_Notes": Fed_Board_Notes,
    "Fed_Boston": Fed_Boston,
    "Fed_Chicago": Fed_Chicago,
    "Fed_Cleveland": Fed_Cleveland,
    "Fed_Dallas": Fed_Dallas,
    "Fed_NewYork": Fed_NewYork,
    "Fed_Richmond": Fed_Richmond,
    "Fed_SanFrancisco": Fed_SanFrancisco,
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
    if scraper_status[name] == "on":
        try:
            # Append the result of each scrape to the list
            print(f"running {name}.py ...")
            dfs.append(scraper.scrape())
            print(f"-----\n Data Scrape: ({i+1}/{total_tasks}) tasks done\n-----")
        except Exception as e:
            print(f"Error occurred while running {name}.py: {e}")
            print(f"Turning off {name}.py for future runs.")
            scraper_status[name] = "off"
    else: # when scraper_status[name] == "off":
        print(f"{name}.py: Skipped execution because script is turned off.")
        print(f"-----\n Data Scrape: ({i+1}/{total_tasks}) tasks done\n-----")

# Write the updated scraper_status back to the file
write_scraper_status("scraper_status.txt", scraper_status)

# Concatenate all data frames in the list into a single data frame
df = pd.concat(dfs, ignore_index=False)

# Part 2: Comparing to historical data
print(f"--------------------\n Part 2: Comparing to Historical Data \n--------------------")

# Calling the compare function from historic/compare.py
compare_historic(df)
print("compare.py complete.")


print(f"--------------------\n Script has completed running. \n--------------------")

