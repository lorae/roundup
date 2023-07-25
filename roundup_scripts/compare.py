# compare.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 24 Jul 2023

import pandas as pd
import os
import ast

from datetime import datetime


def compare_historic(df):
    # Create filepath for output files
    current_date = datetime.now().strftime('%Y-%m-%d-%H%M')
    filepath = f'historic/weekly_data/{current_date}'
    
    # Open "papers-we-have-seen.txt" which contains the unique indices of all papers observed to date
    with open('historic/papers-we-have-seen.txt','r') as f:
        # save entries as historic_set
        historic_set = ast.literal_eval(f.read()) 
    # Use the indices from df to create recent_set
    recent_set = set(df.index)
    
    # Generate the novel set
    novel_set = recent_set - historic_set
    
    # Save novel data txt
    with open(f'{filepath}.txt','w') as f:
        f.write(str(novel_set))
    # Convert the set to a list and get the relevant rows from the df. Then
    # save as csv using filepath
    df.loc[list(novel_set)].to_csv(f'{filepath}.csv')
    
    # Overwrite the historical with the new data
    with open('historic/papers-we-have-seen.txt','w') as f:
        f.write(str(historic_set | recent_set))  # union of the two sets  
  