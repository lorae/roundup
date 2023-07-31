### BFI.py ###
# The purpose of this script is to scrape metadata from the most recent BFI working papers. This script uses
# the BFI RSS feed. Numbers are found on the specific landing pages corresponding to each individual paper.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 30 Jul 2023

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://bfi.uchicago.edu/working-papers/"
soup = BeautifulSoup(requests.get(url).content, 'html.parser')

elements = soup.select('div.teaser.teaser--working-paper')

# Get titles, links, dates, and authors from the main website
Titles = [el.select('h2.teaser__title')[0].text.strip() for el in elements]
Links = [el.select('h2.teaser__title a')[0]['href'] for el in elements]
Dates = [el.select('span.meta__date')[0].text.strip() for el in elements]
Authors = [el.select('div.teaser__names')[0].text.strip() for el in elements]
Numbers = ['NA' for _ in elements]

# Get the abstracts
Abstracts = [BeautifulSoup(requests.get(link).content, 'html.parser').select('div.textblock')[0].text.strip() for link in Links]

# Create a dictionary of the six lists, where the keys are the column names.
data = {'Title': Titles,
        'Link': Links,
        'Date': Dates,
        'Author': Authors,
        'Number': Numbers,
        'Abstract': Abstracts}

# Create a DataFrame from the dictionary.
df = pd.DataFrame(data)

'''
print(df)
print(df["Titles"])
print(df["Links"])
print(df["Dates"])
print(df["Authors"])
print(df["Numbers"])
'''

    
