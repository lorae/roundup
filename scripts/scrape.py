# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 2 Mar 2023
# https://realpython.com/beautiful-soup-web-scraper-python/

import requests
from bs4 import BeautifulSoup
import feedparser
import pandas as pd

# Define functions
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
    return [get_element(df, link, 1) for link in df['Link']]

'''
Note to self: I can make this third function cleaner by trying to leverage the fact it is almost the same
as get_element
'''
def get_numbers(df):
    return [get_soup(link) # Get the HTML content of the page at the current link and parse it using BeautifulSoup
            .find('div', {'class': 'page-content'})  # Find the 'div' tag with class 'page-content'
            .text # Extract the text of the 'div' tag
            .strip() # Remove any leading/trailing whitespace from the text
            .split('\n')[0] # Split the text by newline character '\n' and return the third element (the abstract)
            .replace("Staff Working Paper No. ", "") # remove unnecessary text
            .replace(",", "") # remove unnecessary commas
            for link in df["Link"]]  # Iterate over each link in the dataframe

# Main code
URL = "https://www.bankofengland.co.uk/rss/publications"
f = feedparser.parse(URL)

data = [(entry.title,
         entry.link,
         entry.published) #creates a tuple containing the title, link, publication date, and summary for the current entry
        for entry in f.entries #introduce a loop that iterates over each entry in the RSS feed (f.entries)
        if "working paper" in entry.summary] #filters the entries based on whether the phrase "working paper" appears in the summary

df = pd.DataFrame(data, columns=["Title", "Link", "Date"])
df["Abstract"] = get_abstracts(df)
df["Author"] = get_authors(df)
df["Number"] = get_numbers(df)

print(df)

# save the data frame to a JSON file
df.to_json('data.json', orient='records')
print("df saved to json")

# load the data frame from the JSON file
df_loaded = pd.read_json('data.json')
print("df_loaded loaded from json")
