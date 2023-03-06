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

Title = [a.text for a in soup.select('.teaser__title a')]
print(Title)
Date = [pd.to_datetime(date.get_text(strip=True), format='%b %d, %Y').strftime('%B %d, %Y') for date in soup.select('.meta__date')]
print(Date)
Author = [name.get_text(strip=True) for name in soup.select('.person-list__names')]
print(Author)
#The links don't work properly
Link = [a['href'] for a in soup.select('a.button.clear') if 'https://bfi.uchicago.edu/working-paper/' in a['href']]
print(Link)


def get_abstract(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    abstract = soup.select_one('div[itemprop="articleBody"] p').get_text(strip=True)
    return abstract

Abstract = [get_abstract(link) for link in Link]

BFI = pd.DataFrame({
    'Title': Title,
    'Author': Author,
    'Date': Date,
    'Abstract': Abstract,
    'Link': Link,
    'Source': 'BFI'
})
BFI.to_pickle('output/BFI.pkl')  # Save as a pickle file instead of RDS
