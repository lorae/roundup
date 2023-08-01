# Fed-Chicago.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 21 Jun 2023

# https://www.chicagofed.org/publications/publication-listing?filter_series=18
# series = 18 indicates working papers

import requests
from bs4 import BeautifulSoup
import feedparser
import pandas as pd


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


# I define the function "scrape" in every webscraper. That way, in runall.py, it is easy to call BOE.scrape()
# or NBER.scrape(), for instance, knowing that they all do the same thing - namely, navigate to their respective 
# websites and extract the data.
def scrape():
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
    
    # Instead of the data frame having row names (indices) equalling 1, 2, etc,
    # we set them to be an identifier that is unique. In the case of Chicago, we combine
    # Chicago with the number of the paper (eg. 999) to get an identifier Chicago999 that
    # is completely unique across all papers scraped.
    df["Source"] = "FED-CHICAGO"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None
    
    print(df)
    return(df)
