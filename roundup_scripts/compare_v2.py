# compare_v2.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 24 Jul 2023

import pandas as pd
import os
import ast

with open('test-delete-me-later.txt','w') as f:
   f.write(str({"CHICAGO2023-15", "BOE1024"}))  # set of numbers & a tuple


with open('test-delete-me-later.txt','r') as f:
   my_set = ast.literal_eval(f.read())
