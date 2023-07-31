### Board.py ###
# The purpose of this script is to scrape metadata from the most recent Fed Board working papers. This script uses
# the Federal Reserve Board of Governors working paper landing page. 
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 31 Jul 2023

import requests
from bs4 import BeautifulSoup
import pandas as pd
def scrape():
    url = "https://www.federalreserve.gov/econres/feds/index.htm"
    headers = { # if we do not spoof a browser, the website will not provide data
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    # Select all div elements with classes "col-xs-12", "col-md-9", and "heading" 
    # that do not have a "style" attribute. This effectively excludes the first 
    # element on the page which has the "style" attribute.
    elements = soup.select('div.col-xs-12.col-md-9.heading:not([style])')

    # Get titles, links, dates, and authors from the main website. Format them as a dictionary.
    data = {
        'Title': [el.select_one('h5 > a').text.strip() for el in elements],
        'Link': ["https://www.federalreserve.gov" + el.select_one('h5 > a')['href'] for el in elements],
        'Number': [el.select_one('span.badge').text.strip().replace('FEDS ', '') for el in elements],
        'Author': [el.select_one('div.authors').text.strip() for el in elements],
        'Abstract': [el.select_one('div.collapse > p').text.strip().replace('Abstract: ', '') for el in elements],
        'Date': [el.select_one('time')['datetime'] for el in elements]
    }

    # Create a DataFrame from the dictionary.
    df = pd.DataFrame(data)


    # Instead of the data frame having row names (indices) equalling 1, 2, etc,
    # we set them to be an identifier that is unique. In the case of Chicago, we combine
    # Chicago with the number of the paper (eg. 999) to get an identifier Chicago999 that
    # is completely unique across all papers scraped.
    df.index = "BOARD" + df['Number'].astype(str)
    df.index.name = None

    print(df)
    return(df)
