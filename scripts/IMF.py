### IMF.py ###
# The purpose of this script is to scrape metadata from the most recent IMF working papers
# from the IMF website.
# This paper uses the IMF RSS feed.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# Created: 2 Mar 2023

### this code needs a lot of work.

import requests
from bs4 import BeautifulSoup
import feedparser
import pandas as pd

# Define functions
def get_soup(url):
    page = requests.get(url) # Get the HTML content of the page at the current link
    soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content using BeautifulSoup
    return soup

def get_element(df, link, index):
    return [get_soup(link) # Get the HTML content of the page at the current link and parse it using BeautifulSoup
            .find('div', {'class': 'page-content'})  # Find the 'div' tag with class 'page-content'
            .text # Extract the text of the 'div' tag
            .strip() # Remove any leading/trailing whitespace from the text
            .split('\n')[index]] # Split the text by newline character '\n' and return the third element (the abstract)

def get_abstracts(df):
    return [get_element(df, link, 2) for link in df['Link']]

def get_authors(df):
    return [get_element(df, link, 1)[0]
            .replace("By", "") # remove unnecessary text
            .replace("[", "") # remove unnecessary brackets
            .replace("]", "") # remove unnecessary brackets
            .strip() # Remove any leading/trailing whitespace from the text
            for link in df["Link"]]

def get_numbers(df):
    return [get_element(df, link, 0)[0]
            .replace("Staff Working Paper No. ", "") # remove unnecessary text
            .replace(",", "") # remove unnecessary commas
            for link in df["Link"]]

# Main code
URL = "https://www.imf.org/en/Publications/RSS?language=eng&series=IMF%20Working%20Papers"
f = feedparser.parse(URL)

data = [(entry.title,
         entry.link,
         entry.published) #creates a tuple containing the title, link, publication date, and summary for the current entry
        for entry in f.entries]

df = pd.DataFrame(data, columns=["Title", "Link", "Date"])

'''
df["Abstract"] = get_abstracts(df)
df["Author"] = get_authors(df)
df["Number"] = get_numbers(df)

print(df)

# save the data frame to a JSON file
df.to_json('../processed_data/BOE.json', orient='records')
print("df saved to json")

# load the data frame from the JSON file
df_loaded = pd.read_json('../processed_data/BOE.json')
print("df_loaded loaded from json")

'''
