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

# Initialize the lists
titles = []
links = []
dates = []
abstracts = []
authors = []
numbers = []

# Get titles, links, dates, and authors from the main website. Note
# that BFI papers are not numbered, so "numbers" will be populated
# with NA.
for element in soup.select('div.teaser.teaser--working-paper'):
    title = element.select('h2.teaser__title')[0].text.strip()
    titles.append(title)
    
    link = element.select('h2.teaser__title a')[0]['href']
    links.append(link)
    
    date = element.select('span.meta__date')[0].text.strip()
    dates.append(date)
    
    author = element.select('div.teaser__names')[0].text.strip()
    authors.append(author)
    
    number = 'NA' #BFI doesn't number their working papers
    numbers.append(number)

# Navigate to each page's link to get the abstracts
for link in links:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    abstract = soup.select('div.textblock')[0].text.strip()
    abstracts.append(abstract)

# create a dictionary of the six lists, where the keys are the column names
data = {'Title': titles, 'Link': links, 'Date': dates, 'Author': authors, 'Number': numbers, 'Abstract': abstracts}

# create a DataFrame from the dictionary
df = pd.DataFrame(data)

# save the data frame to a JSON file
df.to_json('../processed_data/BFI.json', orient='records')
print("df saved to json")

# load the data frame from the JSON file
df_loaded = pd.read_json('../processed_data/BFI.json')
print("df_loaded loaded from json")
    
    
