### BFI.py ###
# The purpose of this script is to scrape metadata from the most recent BFI working papers. This script uses
# the BFI RSS feed.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# Created: 6 Mar 2023

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://bfi.uchicago.edu/working-papers/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# Get titles, links, dates, and authors from the main website. Note that
# BFI papers are not numbered, so "numbers" is populated with NA.
titles = [element.select('h2.teaser__title')[0].text.strip()
          for element in soup.select('div.teaser.teaser--working-paper')]

links = [element.select('h2.teaser__title a')[0]['href']
         for element in soup.select('div.teaser.teaser--working-paper')]

dates = [element.select('span.meta__date')[0].text.strip()
         for element in soup.select('div.teaser.teaser--working-paper')]

authors = [element.select('div.teaser__names')[0].text.strip()
           for element in soup.select('div.teaser.teaser--working-paper')]

numbers = ['NA'
           for element in soup.select('div.teaser.teaser--working-paper')]

# Initalize "abstracts" list
abstracts = []
# Navigate to each page's link to get the abstracts. (I could have used list
# comprehension here, but I felt like the classic "for" loop is easier to read).
for link in links:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    abstract = soup.select('div.textblock')[0].text.strip()
    abstracts.append(abstract)

# Create a dictionary of the six lists, where the keys are the column names.
data = {'Title': titles,
        'Link': links,
        'Date': dates,
        'Author': authors,
        'Number': numbers,
        'Abstract': abstracts}

# Create a DataFrame from the dictionary.
df = pd.DataFrame(data)

# Save the DataFrame to a JSON file.
df.to_json('../processed_data/BFI.json', orient='records')
print("df saved to json")

# Load the DataFrame from the JSON file.
df_loaded = pd.read_json('../processed_data/BFI.json', orient='records')
print("df_loaded loaded from json")

    
