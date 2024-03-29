# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 21 Jun 2023
# https://realpython.com/beautiful-soup-web-scraper-python/

import requests
from bs4 import BeautifulSoup
import feedparser
import pandas as pd


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
    
    # Choose the longest potential abstract and remove the leading and trailing character (which is a [ and ])
    abstract = max(potential_abstracts, key=len) if potential_abstracts else None

    return abstract


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

# I define the function "scrape" in every webscraper. That way, in runall.py, it is easy to call BOE.scrape()
# or NBER.scrape(), for instance, knowing that they all do the same thing - namely, navigate to their respective 
# websites and extract the data.
def scrape():
    # Let's start by going to the RSS feed and extracting the data
    URL = "https://www.bankofengland.co.uk/rss/publications"
    f = feedparser.parse(URL)

    # Now we grab the data that's easy to get directly from the RSS feed
    data = [(entry.title,
             entry.link,
             entry.published[:-14]) #creates a tuple containing the title, link, publication date, and summary for the current entry
            for entry in f.entries #introduce a loop that iterates over each entry in the RSS feed (f.entries)
            if "working paper" in entry.summary] #filters the entries based on whether the phrase "working paper" appears in the summary

    # The trickier operations are conducted using functions defined above
    df = pd.DataFrame(data, columns=["Title", "Link", "Date"])
    df["Abstract"] = get_abstracts(df)
    df["Author"] = get_authors(df)
    df["Number"] = get_numbers(df)

    # Instead of the data frame having row names (indices) equalling 1, 2, etc,
    # we set them to be an identifier that is unique. In the case of BOE, we combine
    # BOE with the number of the paper (eg. 999) to get an identifier BOE999 that
    # is completely unique across all papers scraped.
    df["Source"] = "BOE"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None
    
    print(df)
    return(df)

