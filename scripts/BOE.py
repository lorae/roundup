# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 20 Jun 2023
# https://realpython.com/beautiful-soup-web-scraper-python/

import requests
from bs4 import BeautifulSoup
import feedparser
import pandas as pd

# Define functions
def get_soup(url):
    # In order for the code to run, it is necessary to spoof a browser. Otherwise, the website will not provide the information
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    page = requests.get(url, headers=headers) # Include headers in request
    soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content using BeautifulSoup
    return soup


def get_element(df, link, index):
    return [get_soup(link) # Get the HTML content of the page at the current link and parse it using BeautifulSoup
            .find('div', {'class': 'page-content'})  # Find the 'div' tag with class 'page-content'
            .text # Extract the text of the 'div' tag
            .strip() # Remove any leading/trailing whitespace from the text
            .split('\n')[index]] # Split the text by newline character '\n' and return the third element (the abstract)

def get_abstract(df, link):
    soup = get_soup(link)
    abstract_tags = soup.find('div', {'class': 'page-content'}).find_all(['p', 'div'], recursive=False)

    potential_abstracts = []
    for tag in abstract_tags:
        # Check if this is the download button. The abstract always appears before the download button on the webpage
        if tag.find('a', {'class': 'btn btn-pubs btn-has-img btn-lg'}):
            break
        potential_abstracts.append(tag.text.strip())
    
    # Choose the longest potential abstract
    abstract = max(potential_abstracts, key=len) if potential_abstracts else None
    return [abstract]


def get_abstracts(df):
    return [get_abstract(df, link) for link in df['Link']]

'''
def get_abstracts(df):
    return [get_element(df, link, 2) for link in df['Link']]
'''
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
df.to_json('processed_data/BOE.json', orient='records')
print("df saved to json")

# load the data frame from the JSON file
df_loaded = pd.read_json('processed_data/BOE.json')
print("df_loaded loaded from json")

''' Only un-comment this line for troubleshooting purposes
# load to a CSV to check if it looks good
df_loaded.to_csv('output.csv')
'''
