### ECB.py ###
# The purpose of this script is to scrape metadata from the most recent ECB working papers. This script uses
# the ECB website.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 1 September 2023

from bs4 import Tag, BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import pandas as pd

def get_soup(url): 
    # Create a new instance of the Firefox driver
    driver = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Run Firefox in headless mode.
    driver = webdriver.Firefox(options=options)

    # Go to the page
    driver.get(url)
    time.sleep(5)
    
    # Use WebDriverWait to wait for the element to become clickable
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "snippet1"))
        )
        # Scroll to the element
        driver.execute_script("arguments[0].scrollIntoView();", element)
    except Exception as e:
        print(f"An error occurred: {e}")   
    time.sleep(5) # It still needs some extra time to load

    # Get the page source and parse it
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close the driver
    driver.quit()

    return soup

# I define the function "scrape" in every webscraper. That way, in runall.py, it is easy to call BOE.scrape()
# or NBER.scrape(), for instance, knowing that they all do the same thing - namely, navigate to their respective 
# websites and extract the data.
def scrape(): 
    url = "https://www.ecb.europa.eu/pub/research/working-papers/html/index.en.html"

    soup = get_soup(url)

    elements = soup.find('dl', {'class': 'ecb-basicList wpSeries ecb-lazyload pub-list-filter'})

    # Filter so that we keep only the <dt> tags that have the 'isodate' attribute (if they do not
    # have this attribute, then they do not correspond with data we care about, so we discard them).
    filtered_dt_elements = [dt for dt in elements.find_all('dt') if dt.has_attr('isodate')]

    # Initialize lists to store data
    Date = []
    Title = []
    Author = []
    Abstract = []
    Link = []
    Number = []

    # Loop through the filtered <dt> and corresponding <dd> tags.  <dt> tags contain the date.
    # All other information is in the <dd> tags.
    for dt in filtered_dt_elements[:20]: # only selecting first 20 elements - we don't need them all
        dd = dt.find_next_sibling('dd')  
        if not dd:
            continue

        # Date (from dt tag)
        date_div = dt.find('div', class_='date')
        date = date_div.text if date_div else "No date"
        Date.append(date)

        # Title
        title_div = dd.find('div', class_='title')
        title = title_div.text if title_div else "No title"
        Title.append(title)

        # Author
        author_list = dd.find_all('li')
        author = ', '.join([li.text for li in author_list]) if author_list else "No authors"
        Author.append(author)

        # Abstract
        abstract_dd = dd.find('dd')
        abstract = abstract_dd.text if abstract_dd else "No abstract"
        Abstract.append(abstract)

        # Link
        if title_div:
            link_a = title_div.find('a')
            link = "https://www.ecb.europa.eu"+ link_a['href'] if link_a else "No link"
        else:
            link = "No link"
        Link.append(link)

        # Number
        number_div = dd.find('div', {'class': 'category'})
        number = number_div.text.replace("No. ", "") if number_div else "No number"
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
    df["Source"] = "ECB"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None

    print(df)
    return(df)

