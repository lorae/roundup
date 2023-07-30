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

print(BEA.scrape())
