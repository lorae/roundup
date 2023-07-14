# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 21 Jun 2023

# https://www.chicagofed.org/publications/publication-listing?filter_series=18
# series = 18 indicates workind papers

import requests
from bs4 import BeautifulSoup
import feedparser
import pandas as pd

# First, print a progress message
print("Running Chicago.py")

# Define functions
def get_soup(url): # Used to get the initial soup from the main URL that lists all the papers
    # In order for the code to run, it is necessary to spoof a browser. Otherwise, the website will not provide the information
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    page = requests.get(url, headers=headers) # Include headers in request
    soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content using BeautifulSoup
    return soup

def get_elements(url): # Used to parse the data on the main URL for a list of the most recent papers, including title,
    # link, author, and number
    soup = get_soup(url) 
    elements = soup.find_all('div', {'class': 'cfedPublicationListing'})  
    return elements

def get_abstract(link): 
    soup = get_soup(link)
    abstract_tags = soup.find('div', {'class': 'cfedArticle__introParagraph'})
    if abstract_tags:
        return abstract_tags.text.strip()  # return the text
    else:
        return None  # return None if the tag is not found

def get_abstracts(df):
    return [get_abstract(link) for link in df['Link']]


URL = "https://www.chicagofed.org/publications/publication-listing?filter_series=18"
elements = get_elements(URL)

# First pass where we get the list of elements from the URL and extract relevant information
data = []
for element in elements:
    # The name of the tag we use to get the title and link
    title_link_tag = element.find('a', {'class': 'cfedPublicationListing--title'})

    # Get the title
    title = title_link_tag.text.strip()
    # Get the link
    link = "https://www.chicagofed.org" + title_link_tag['href']
    # Get the number
    number = link.split("/")[-1]
    # Get the author
    author = element.find('div', {'class': 'cfedPublicationListing--info'}).text.strip().split("|")[0].strip()
    # Here, we're assuming that the year and month are always at index 1 and 4, respectively, in the info_text list.
    # Also, we're assuming that these strings can be safely stripped of whitespace and turned into integers.
    info_text = element.find('div', {'class': 'cfedPublicationListing--info'}).text.strip().split("|")
    author = info_text[0].strip()
    year = str(info_text[1].strip())
    month = info_text[4].strip()
    date = month + " " + year

    # Combine this all together
    data.append((title, link, date, author, number))

df = pd.DataFrame(data, columns=["Title", "Link", "Date", "Author", "Number"])


# Next pass where we add abstracts to the df
df["Abstract"] = get_abstracts(df)

# Reorder the data frame
df = df[['Title', 'Author', 'Abstract', 'Link', 'Number', 'Date']]

# save the data frame to a JSON file
df.to_json('processed_data/Chicago.json', orient='records')
print("df saved to json")

# load the data frame from the JSON file
df_loaded = pd.read_json('processed_data/Chicago.json')
print("df_loaded loaded from json")

# Only un-comment this line for troubleshooting purposes
# load to a CSV to check if it looks good
'''
df_loaded.to_csv('output.csv')
'''

# Only un-comment this line to print df in long format. Otherwise will print in short format
'''
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.expand_frame_repr', False, 'display.max_colwidth', -1):
    print(df)
'''
print(df_loaded)

# Make a historical file by taking just the less recent entries and saving
pseudo_hist = df_loaded.tail(8)
pseudo_hist.to_json('historic_data/Chicago.json', orient='records')

# Finally, print a progress message
print("Chicago.py has finished running")

