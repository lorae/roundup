# Fed_SanFrancisco.py
# The purpose of this script is to scrape metadata from the most recent San Francisco Fed working papers. This script uses
# the SF Fed's Working Paper landing page.
# Lorae Stojanovic
#
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 14 Aug 2023

from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd

def get_soup(url): 
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()
    # Go to the page
    driver.get(url)
    time.sleep(5)
    # Get the page source and parse it
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Don't forget to close the driver
    driver.quit()

    return soup

def scrape():
    url = "https://www.frbsf.org/economic-research/publications/working-papers/"

    # Get the soup
    soup = get_soup(url)

    #print(soup)

    # We only need the most recent 40 or so working papers... no need to get them all the way back from 2001.
    elements = soup.find_all('article', {'class': 'cf'})[1:30]

    # Initialize lists
    Title = []
    Link = []
    Number = []
    Author = []
    Date = []
    Abstract = []

    for el in elements:
        title = el.find('a')['title'].strip()
        Title.append(title)
            
        link = "https://www.frbsf.org" + el.find('a')['href']
        Link.append(link)
        
        number = link.split("working-papers/")[1][:-1].replace("/", "-")
        Number.append(number)
        
        date = el.find('meta', itemprop = 'datePublished')['content']
        Date.append(date)
        
        author = el.find('meta', itemprop = 'name')['content']
        Author.append(author)
        
        abstract = el.find('div', class_= 'collapsible').get_text().strip()
        Abstract.append(abstract)

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
    df["Source"] = "FED-SANFRANCISCO"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None

    print(df)
    return(df)