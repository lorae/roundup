# Fed_Board_Notes.py
# The purpose of this script is to scrape metadata from the most recent Fed Board "Feds Notes". This script uses
# the Federal Reserve Board of Governors "Fed Notes" landing page.
# Lorae Stojanovic
#
# Note: this will scrape from the current year and the year prior if the month == January 
#
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 11 Aug 2023

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def get_soup(url): # Used to get the initial soup from the main URL that lists all the papers
    # In order for the code to run, it is necessary to spoof a browser. Otherwise, the website will not provide the information
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    page = requests.get(url, headers=headers) # Include headers in request
    soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content using BeautifulSoup
    return soup

def scrape():
    url_list = ["https://www.federalreserve.gov/econres/notes/feds-notes/default.htm"]
    # Get the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month

    # If the current month is January, also look at last year's entries.
    if current_month == 1:
        # Create a URL for the current year
        last_year_url = f"https://www.federalreserve.gov/econres/notes/feds-notes/{current_year-1}-index.htm"
        url_list += last_year_url

    print(url_list)

    # Initialize lists
    Title = []
    Link = []
    Number = []
    Author = []
    Date = []
    Abstract = []

    for url in url_list:
        soup = get_soup(url)
        #print(soup)
        
        elements = soup.select('div.col-xs-12.col-md-9.heading.feds-note:not([style])')
        #print(elements)
        
        for el in elements:
            title = el.find('h5').text.strip()
            Title.append(title)
            
            author = el.find('div', class_='authors').text.strip()
            Author.append(author)
            
            date = el.find('time')['datetime']
            Date.append(date)
            
            abstract = el.find_all('p')[1].text.strip()
            Abstract.append(abstract)
            
            # second p element, slice off the first 4 chars (that say "DOI:")
            link = el.find_all('p')[2].text[4:].strip()
            Link.append(link)
            
            # These don't have numbers, so I will make them the end part of
            # the DOI url
            number = link.split(".org")[1].replace(".", "").replace("/", "").replace("-", "").strip()
            Number.append(number)
            
    # Create a dictionary of the six lists, where the keys are the column names.
    data = {'Title': Title,
            'Link': Link,
            'Date': Date,
            'Author': Author,
            'Number': Number,
            'Abstract': Abstract}

    # Create a DataFrame from the dictionary.
    df = pd.DataFrame(data)

    # Instead of the data frame having row names (indices) equalling 1, 2, etc,
    # we set them to be an identifier that is unique. In the case of Chicago, we combine
    # Chicago with the number of the paper (eg. 999) to get an identifier Chicago999 that
    # is completely unique across all papers scraped.
    df["Source"] = "FED-BOARD-NOTES"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None

    print(df)
    return(df)