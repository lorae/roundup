# Fed_SanFrancisco.py
# The purpose of this script is to scrape metadata from the most recent San Francisco Fed working papers. This script uses
# the SF Fed's API.
# Lorae Stojanovic
#
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 21 Aug 2023

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
import pandas as pd
import requests
import json

def scrape():
    # Define the URL for the SF Fed working papers API
    URL = 'https://www.frbsf.org/wp-json/wp/v2/sffed_publications?publication-type=1979&per_page=10'

    # Make a GET request to the SF Fed working paper API and parse the JSON response
    data = json.loads(requests.get(URL).text)

    # Create a Pandas DataFrame from the extracted data, with the "Long Abstract" extracted from the paper's URL using XPath
    df = pd.DataFrame({
        'Title': [d['title']['rendered'] for d in data],
        'Link': [d['link'] for d in data],
        'Date': [d['date'].split('T')[0] for d in data], # Extract only the date, not the time
        # Select d['content']['rendered'], which is an HTML object. Parse with Beautiful Soup and then only keep
        # the text within the first <p> tag. (Sometimes there is a second <p> tag, usually containing information
        # about how to download the pdf appendix).
        'Abstract': [BeautifulSoup(d['content']['rendered'], 'html.parser').find('p').text.strip() for d in data],
        'Author': [d['meta']['publication_authors'] for d in data],
        'Number': [d["meta"]["publication_volume"] + "-" + d["meta"]["publication_issue"] for d in data]
    }).sort_values(by='Number')


    # Instead of the data frame having row names (indices) equalling 1, 2, etc,
    # we set them to be an identifier that is unique. In the case of NBER, we combine
    # NBER with the number of the paper (eg. 999) to get an identifier NBER999 that
    # is completely unique across all papers scraped.
    df["Source"] = "FED-SANFRANCISCO"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None
        
    print(df)
    return(df)