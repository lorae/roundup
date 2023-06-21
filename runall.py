# runall.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 21 Jun 2023

import os
import subprocess

print(os.getcwd())

# Path to venv python
venv_python_path = "C:/Users/LStojanovic/Downloads/roundup/venv/Scripts/python.exe"

subprocess.call([venv_python_path, "scripts/BOE.py"])
subprocess.call([venv_python_path, "scripts/Chicago.py"])


