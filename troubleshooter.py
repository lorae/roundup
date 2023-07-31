# troubleshooter.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 27 Jul 2023

# The purpose of this script is to run individual scrape functions to see
# what is wrong

import os
import subprocess
import pandas as pd
from roundup_scripts.compare import compare_historic # User-defined

# Here, we import all the scripts from roundup_scripts/scrapers
import sys
sys.path.append('roundup_scripts/scrapers')
import BEA
import BIS
import BOE
import Chicago
import ECB
import IMF
import NBER

print(os.getcwd())

# Path to venv python
venv_python_path = "C:/Users/stoja/roundup/venv/Scripts/python.exe"
#venv_python_path = "C:/Users/LStojanovic/Downloads/roundup/venv/Scripts/python.exe" #maybe?
#venv_python_path = "/Users/dr.work/Dropbox/Code_Dropbox/Brookings/lorae_roundup/roundup/proj_env/bin/python"


sys.path.append('roundup_scripts/scrapers')
import BFI

#print(BEA.scrape())

import subprocess
subprocess.run([venv_python_path, "roundup_scripts/scrapers/BFI.py"])

