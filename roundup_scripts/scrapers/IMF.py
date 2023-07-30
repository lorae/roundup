### IMF.py ###
# The purpose of this script is to scrape metadata from the most recent IMF working papers. This script uses
# the IMF RSS feed.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 30 Jul 2023

import requests
from bs4 import BeautifulSoup
import feedparser
import pandas as pd
from lxml import html
import re

# NOTE: The purpose of defining the function get_element (rather than just using get_abstracts, get_authors,
# and get_numbers) is to parse the HTML for each webpage only once, rather than 3 times. This significantly
# reduces the run time of this script.

def get_element(df):
    elements = []
    # Iterate over each link in the input df
    for link in df['Link']:
        # Make an HTTP request to the link and parse the HTML content
        response = requests.get(link)
        tree = html.fromstring(response.content)
        # Append the HTML tree to the list of elements
        elements.append(tree)
    # Return the list of elements (which is a list of HTML trees)
    return elements

def get_abstracts(elements):
    # Use list comprehension to extract the abstracts from the HTML trees using XPath
    return [tree.xpath('/html/body/div[3]/main/article/div[1]/div/section[1]/p[8]/text()')[0]
            for tree in elements]


def get_authors(elements):
    # Use list comprehension to extract the authors from the HTML trees using XPath
    # Clean up the author names and separate them with commas using regular expressions
    # Then join them into a single string
    return [
        ', '.join([
            re.sub(r'\s*;\s*', ', ', author.text_content().strip()) 
            for author in tree.xpath('/html/body/div[3]/main/article/div[1]/div/section[1]/p[2]')
        ]) for tree in elements
    ]

def get_numbers(elements):
    # Use list comprehension to extract the numbers from the HTML trees using XPath
    # Remove leading/trailing whitespace using the .strip() method
    return [tree.xpath('/html/body/div[3]/main/article/div[1]/div/section[3]/div/p[6]')[0]
            .text_content().strip()
            for tree in elements]

# I define the function "scrape" in every webscraper. That way, in runall.py, it is easy to call BOE.scrape()
# or NBER.scrape(), for instance, knowing that they all do the same thing - namely, navigate to their respective 
# websites and extract the data.
def scrape():
    URL = "https://www.imf.org/en/Publications/RSS?language=eng&series=IMF%20Working%20Papers"
    f = feedparser.parse(URL)

    data = [(entry.title,
             entry.link,
             entry.published) #creates a tuple containing the title, link, publication date, and summary for the current entry
            for entry in f.entries]

    # Create a pandas data frame from the extracted data
    df = pd.DataFrame(data, columns=["Title", "Link", "Date"])
    #print("IMF titles, links, and dates have been gathered.")

    # Extract the HTML content for each link in the data frame using the get_element() function
    elements = get_element(df)

    # Extract the abstracts, authors, and numbers for each HTML tree using get_abstracts, get_authors,
    # and get_numbers
    df["Abstract"] = get_abstracts(elements)
    #print("... abstracts have been gathered.")
    df["Author"] = get_authors(elements)
    #print("... authors have been gathered.")
    df["Number"] = get_numbers(elements)
    #print("... numbers have been gathered.")

    # Instead of the data frame having row names (indices) equalling 1, 2, etc,
    # we set them to be an identifier that is unique. In the case of Chicago, we combine
    # Chicago with the number of the paper (eg. 999) to get an identifier Chicago999 that
    # is completely unique across all papers scraped.
    df.index = "IMF" + df['Number'].astype(str)
    df.index.name = None

    print(df)
    return(df)

