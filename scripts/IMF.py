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
from lxml import html
import re

def get_element(df, x):
    # Define an empty list to hold the elements
    elements = []
    # Iterate over each link in the input DataFrame
    for link in df['Link']:
        # Make an HTTP request to the link and parse the HTML content
        response = requests.get(link)
        tree = html.fromstring(response.content)
        # Extract the element from the HTML content and append it to the list
        element = tree.xpath(x)
    # Return the list of elements
    return elements

    
def get_abstracts(df):
    # Define an empty list to hold the abstracts
    abstracts = []
    # Iterate over each link in the input DataFrame
    for link in df['Link']:
        # Make an HTTP request to the link and parse the HTML content
        response = requests.get(link)
        tree = html.fromstring(response.content)
        # Extract the abstract from the HTML content and append it to the list of abstracts
        abstract = tree.xpath('/html/body/div[3]/main/article/div[1]/div/section[1]/p[8]/text()')[0]
        abstracts.append(abstract)
    # Return the list of abstracts
    return abstracts


def get_authors(df):
    # Define an empty list to hold the list of authors for each link
    authors_list = []
    # Iterate over each link in the input DataFrame
    for link in df['Link']:
        # Make an HTTP request to the link and parse the HTML content
        response = requests.get(link)
        tree = html.fromstring(response.content)
        # Extract the list of author elements from the HTML content
        author_elems = tree.xpath('/html/body/div[3]/main/article/div[1]/div/section[1]/p[2]')
        # Clean up the author names and separate them with commas
        authors = [re.sub(r'\s+', ' ', author.text_content()) for author in author_elems]
        authors_comma_sep = [re.sub(r'\s*;\s*', ', ', author) for author in authors]
        # Append the list of cleaned up and comma-separated author names to the authors_list
        authors_list.append(authors_comma_sep)
    # Return the list of authors for each link
    return authors_list


def get_numbers(df):
    # Define an empty list to hold the numbers
    numbers = []
    # Iterate over each link in the input DataFrame
    for link in df['Link']:
        # Make an HTTP request to the link and parse the HTML content
        response = requests.get(link)
        tree = html.fromstring(response.content)
        # Extract the numbers element from the HTML content
        numbers_elem = tree.xpath('/html/body/div[3]/main/article/div[1]/div/section[3]/div/p[6]')[0]
        # Extract the text content of the numbers element and remove any leading/trailing whitespace
        numbers_text = numbers_elem.text_content().strip()
        # Append the cleaned up numbers to the numbers list
        numbers.append(numbers_text)
    # Return the list of numbers
    return numbers

# Main code
URL = "https://www.imf.org/en/Publications/RSS?language=eng&series=IMF%20Working%20Papers"
f = feedparser.parse(URL)

data = [(entry.title,
         entry.link,
         entry.published) #creates a tuple containing the title, link, publication date, and summary for the current entry
        for entry in f.entries]

df = pd.DataFrame(data, columns=["Title", "Link", "Date"])
print("IMF titles, links, and dates have been gathered.")


df["Abstract"] = get_abstracts(df)
print("... abstracts have been gathered.")
df["Author"] = get_authors(df)
print("... authors have been gathered.")
df["Number"] = get_numbers(df)
print("... numbers have been gathered.")

print(df)

# save the data frame to a JSON file
df.to_json('../processed_data/IMF.json', orient='records')
print("df saved to json")

# load the data frame from the JSON file
df_loaded = pd.read_json('../processed_data/IMF.json')
print("df_loaded loaded from json")
