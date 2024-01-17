# Fed_StLouis.py
# The purpose of this script is to scrape metadata from the most recent St Louis Fed working papers,
# found at https://research.stlouisfed.org/wp/. This script uses xxx to do yyy.
#
# Lorae Stojanovic
#
# OpenAI's tool, ChatGPT, was used for coding assistance in this project.
# LE: 15 Jan 2024

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

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
    
def scrape():
    url = "https://research.stlouisfed.org/wp/"
    print(url)
    
    # Get the soup
    soup = get_soup(url)
    
    # Find all the elements matching the given XPath
    elements = soup.select('div.seperator-bottom') #The misspelling of "seperator" is faithful to the website
            
    # Initialize lists
    Title = []
    Link = []
    Number = []
    Author = []
    Date = []
    Abstract = []

    for element in elements:
        # Title
        Title += [element.find('a', {'class': 'title'}).text.strip()]
        
        # Link
        Link += ["https://research.stlouisfed.org/" + element.find('a', {'class': 'title'})['href']]
        
        # Author
        author_text = element.find('span', {'class': 'byline'}).text
        author_text = author_text.split("Working Paper")[0]  # Keep the part before "Working Paper"
        author_text = author_text.replace("\n", " ")  # Replace newlines with spaces
        author_text = re.sub(' +', ' ', author_text)  # Replace multiple spaces with a single space
        author_text = re.sub('by', "", author_text)  # Remove the word "by" 
        author_text = author_text.strip()  # Remove leading and trailing spaces
        Author += [author_text]
        
        # Number
        number_text = element.find('span', {'class': 'byline'}).text
        number_text = number_text.split("Working Paper")[1]  # Keep the part after "Working Paper"
        number_text = number_text.split("updated")[0]  # Keep the part before "updated"
        number_text = number_text.split("added")[0]  # Keep the part before "added"
        number = re.sub('-', '', number_text)  # Remove the dash
        number = number_text.strip()  # Remove leading and trailing spaces
        Number += [number]
        
        # Date
        date_text = element.find('span', {'class': 'byline'}).text
        date_text = date_text.split(f"{number}")[1]  # Keep the part after the working paper number
        date_text = re.sub('updated', '', date_text) # Remove "updated"
        date_text = re.sub('added', '', date_text) # Remove "added"
        date_text = date_text.strip()  # Remove leading and trailing spaces
        Date += [date_text]
        
        # Abstract
        Abstract += [element.find_all('p')[1].text.strip()]

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
    df["Source"] = "FED-STLOUIS"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None
        
    print(df)
    return(df)
