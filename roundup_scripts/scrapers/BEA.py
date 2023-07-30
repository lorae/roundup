### BEA.py ###
# The purpose of this script is to scrape metadata from the most recent BEA working papers. This script uses
# the BEA research papers landing page (given by the URL below). Abstracts are found on the specific landing
# pages corresponding to each individual paper.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 30 Jul 2023

import requests
from bs4 import BeautifulSoup
import pandas as pd

# I define the function "scrape" in every webscraper. That way, in runall.py, it is easy to call BOE.scrape()
# or NBER.scrape(), for instance, knowing that they all do the same thing - namely, navigate to their respective 
# websites and extract the data.
def scrape():
    # Define the URL
    url = "https://www.bea.gov/research/papers"

    # Send a GET request to the URL and get the HTML content
    html = requests.get(url).content

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the elements matching the given XPath
    elements = soup.select('div.view-content div.card')

    # Extract the data from each element and store it in a list of dictionaries
    # Note: BEA does a poor job of featuring working paper numbers on its website. Instead,
    # we will have to dive into the PDF versions of the papers to get a reliable working paper
    # number.
    data = []
    for element in elements:
        data.append({
            'Title': element.find('h2', {'class': 'paper-title'}).text.strip(),
            'Link': "https://www.bea.gov/" + element.find('h2', {'class': 'paper-title'}).find('a')['href'],
            'Author': element.find('div', {'class': 'paper-mod-date'}).text.strip(),
            'Date': element.find('div', {'class': 'paper-publication-date'}).text.strip().replace('Published', ''),
            #'Number': element.find('div', {'class': 'views-field views-field-field-id paper-mod-date'}).text.strip(),
            'Abstract': BeautifulSoup(requests.get("https://www.bea.gov/" + element.find('h2', {'class': 'paper-title'}).find('a')['href']).content, 'html.parser').find('p', {'class': 'card-abstract'}).get_text(strip=True)
        })

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data)
    print(df['Number'])
    
    # Instead of the data frame having row names (indices) equalling 1, 2, etc,
    # we set them to be an identifier that is unique. In the case of Chicago, we combine
    # Chicago with the number of the paper (eg. 999) to get an identifier Chicago999 that
    # is completely unique across all papers scraped.
    df.index = "BEA" + df['Number'].astype(str)
    df.index.name = None

    print(df)
    return(df)
