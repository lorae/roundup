### BEA.py ###
# The purpose of this script is to scrape metadata from the most recent BEA working papers. This script uses
# the BEA research papers landing page (given by the URL below). Numbers are found on the specific landing
# pages corresponding to each individual paper.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 1 September 2023

import requests
from bs4 import BeautifulSoup
import pandas as pd
import PyPDF2
import time

def get_soup(url):
    # Note that they are tricky at BEA. I have to keep changing the headers.
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
           'AppleWebKit/537.36 (KHTML, like Gecko) '\
           'Chrome/75.0.3770.80 Safari/537.36'}
           
    # Create a session
    session = requests.Session()  
    
    page = session.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    time.sleep(5)  # Adding a delay of 5 seconds
    return soup


def get_number(link): 
    soup = get_soup(link)
    # We extract the URL of the PDF linked on each individual working paper's webpage, since this URL
    # contains the working paper number. This is easier than reading the text of the PDF.
    number_url = soup.find('h2', class_='card-title').find('a')['href'] # the URL containing the number
    # First we check if the paper is, indeed, a working paper. If it is, its url should contain "BEA-WP"
    if "BEA-WP" in number_url:
        # Split the url to pieces before and after characters "BEA-". Keep only the piece following "BEA-" which
        # contains the working paper number. Remove the ".pdf" at the end.
        return number_url.split("BEA-")[1].replace('.pdf', '')
    else:
        return "not a working paper"  # Labelling this entry so we can remove this row later

def get_numbers(df):
    return [get_number(link) for link in df['Link']]
    
# I define the function "scrape" in every webscraper. That way, in runall.py, it is easy to call BOE.scrape()
# or NBER.scrape(), for instance, knowing that they all do the same thing - namely, navigate to their respective 
# websites and extract the data.
def scrape(): 
    # Define the URL
    url = "https://www.bea.gov/research/papers"

    # Get the soup
    soup = get_soup(url)

    # Find all the elements matching the given XPath
    elements = soup.select('div.view-content div.card')

    # Extract the data from each element and store it in a list of dictionaries
    # Note: BEA does a poor job of featuring working paper numbers on its website. Instead,
    # we will have to navigate to the links to the individual URLs that host each webpage
    data = []
    for element in elements:
        data.append({
            'Title': element.find('h2', {'class': 'paper-title'}).text.strip(),
            'Link': "https://www.bea.gov/" + element.find('h2', {'class': 'paper-title'}).find('a')['href'],
            'Author': element.find('div', {'class': 'paper-mod-date'}).text.strip(),
            # We're extracting the datetime attribute of the time element, splitting the part of the string by the letter
            # "T" (after which the data is formulatic and unhelpful) and keeping only the 0th element (before the split),
            # which contains the date of publication.
            'Date': element.find('time').get('datetime').split("T")[0],
            #'Date': element.find('div', {'class': 'paper-publication-date'}).text.strip().replace('Published', ''),
            #'Number': element.find('div', {'class': 'views-field views-field-field-id paper-mod-date'}).text.strip(),
            'Abstract': BeautifulSoup(requests.get("https://www.bea.gov/" + element.find('h2', {'class': 'paper-title'}).find('a')['href']).content, 'html.parser').find('p', {'class': 'card-abstract'}).get_text(strip=True)
        })

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data)
    
    # Next pass where we add abstracts to the df
    df["Number"] = get_numbers(df)
        
    # Reorder the data frame
    df = df[['Title', 'Author', 'Abstract', 'Link', 'Number', 'Date']]

    # Delete the entries of df for which the paper is not a working paper (likely a report), so we choose to 
    # exclude it.
    df = df[df['Number'] != "not a working paper"]
        
    # Instead of the data frame having row names (indices) equalling 1, 2, etc,
    # we set them to be an identifier that is unique. In the case of Chicago, we combine
    # Chicago with the number of the paper (eg. 999) to get an identifier Chicago999 that
    # is completely unique across all papers scraped.
    df["Source"] = "BEA"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None

    print(df)
    return(df)
