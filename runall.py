# runall.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 21 Jun 2023

import os
import subprocess

print(os.getcwd())

# Path to venv python
venv_python_path = "C:/Users/LStojanovic/Downloads/roundup/venv/Scripts/python.exe"

# Make a list of scripts used in the scraper.
scripts = ["scripts/scrapers/BOE.py",
           "scripts/scrapers/Chicago.py",
           "scripts/scrapers/NBER.py"]

# Progress bar 
total_tasks = len(scripts)
for i, script in enumerate(scripts, start=1):
    subprocess.call([venv_python_path, script])
    print(f"-----\n({i}/{total_tasks}) tasks done\n-----")

'''
subprocess.call([venv_python_path, "scripts/scrapers/BOE.py"])
subprocess.call([venv_python_path, "scripts/scrapers/Chicago.py"])
subprocess.call([venv_python_path, "scripts/scrapers/NBER.py"])
'''

