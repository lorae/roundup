# Fed_Cleveland.py
# The purpose of this script is to scrape metadata from the most recent Cleveland Fed working papers. This script uses
# the Cleveland Fed's Working Paper landing page.
#
# IMPORTANT NOTE on this script. The Cleveland Fed uses the same numbers on papers that have been edited, except for the 
# addition of an "r" to indicate a revision. For example, if Joe Doe and Jane Paine wrote a paper in 2021 with index number
# "WP 21-16", and it were revised in 2023, it would be renumbered as "WP 21-16r". I think - but am not sure - that subsequent
# revisions would also be just labelled as "WP 21-16r". This means that when we see a paper for a second time, it is labelled
# as novel by our compare.py script, since compare.py checks a source and paper # to determine whether something is new. 
# That was an intentional decision on my part when I wrote this code. However, if we choose to treat these revisions
# as non-novel, then the part of the code labelling the paper "Number" will have to be altered. Please keep this in mind if 
# this question comes up in the future.
#
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 22 Aug 2023

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd


def get_soup(url): 
    chrome_service = Service(ChromeDriverManager().install())
    
    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]
    for option in options:
        chrome_options.add_argument(option)

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Go to the page
    driver.get(url)
    
    time.sleep(10)

    # Get the page source and parse it
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Don't forget to close the driver
    driver.quit()

    return soup

def scrape():
    url = "https://www.clevelandfed.org/publications/working-paper"

    # Get the soup
    soup = get_soup(url)

    # Find all the elements matching the given XPath
    elements = soup.find_all('li', {'class': 'result-item'})

    Title = []
    Link = []
    Date = []
    Abstract = []
    Number = []
    Author = []

    for el in elements:
        # Get the title
        title = el.find('h5').text.strip()
        Title.append(title)
           
        # Get the link
        link = el.find('h5').find('a')['href']
        Link.append("https://www.clevelandfed.org" + link)
        
        # Get the number
        # I'd use the link for this, since the links do contain the number, but sometimes the urls
        # have inconsistencies (e.g. writing '23-16' instead of '2316'. I've decided to use a different
        # element to get the number.
        date_number = el.find('div', {'class': 'date-reference'}).get_text().split("|")
        number = date_number[1].replace("WP", "").strip()
        Number.append(number)
        
        # Get the date
        date = date_number[0].strip()
        Date.append(date)
        
        # Get the abstract
        abstract = el.find('div', {'class': 'page-description'}).get_text().strip()
        Abstract.append(abstract)
         
        #Get the authors
        authors_list = el.find('div', {'class': 'authors'}).get_text().strip().split('\n')
        authors_string = ", ".join(authors_list)
        Author.append(authors_string)

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
    df["Source"] = "FED-CLEVELAND"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None

    print(df)
    return(df)