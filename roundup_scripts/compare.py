# compare.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 24 Jul 2023

import pandas as pd
import os
import ast

'''
with open('test-delete-me-later.txt','w') as f:
   f.write(str({"CHICAGO2023-15", "BOE1024"}))  # set of numbers & a tuple
'''
def compare_historic(df):
    # First we open "papers-we-have-seen.txt", a file which contains the unique 
    # indices of all the papers we have seen so far.
    with open('historic/papers-we-have-seen.txt','r') as f:
        historic_set = ast.literal_eval(f.read()) # save entries into historic_set
    print(historic_set)
    
    # Now we insert the indices of the scraped papers from df into recent_set
    recent_set = set(df.index)
    print(recent_set)
    
  