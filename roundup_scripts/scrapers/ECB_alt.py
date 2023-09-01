### ECB.py ###
# The purpose of this script is to scrape metadata from the most recent ECB working papers. This script uses
# the ECB website.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 31 August 2023

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
    driver = webdriver.Firefox()

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

    
def element_conditional():
    # Get the current month
    current_month = datetime.now().month
    current_month = 1

    # If the current month is January
    if current_month == 1:
        elements_list = [0, 1] # check the previous year and the current year
    else:
        elements_list = [0] # check only the current year
    
    return(elements_list)
    
url = "https://www.ecb.europa.eu/pub/research/working-papers/html/index.en.html"

soup = get_soup(url)

elements = soup.find('dl', {'class': 'ecb-basicList wpSeries ecb-lazyload pub-list-filter'})

# Filter so that we keep only the <dt> tags that have the 'isodate' attribute (if they do not
# have this attribute, then they do not correspond with data we care about, so we discard them).
filtered_dt_elements = [dt for dt in elements.find_all('dt') if dt.has_attr('isodate')]


Date = []
Title = []
Author = []
Abstract = []
Link = []
Number = []

# Loop through the filtered <dt> and corresponding <dd> tags.  <dt> tags contain the date.
# All other information is in the <dd> tags.
for dt in filtered_dt_elements[:10]:
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

'''
print(Date)
print(Title)
print(Author)
print(Abstract)
print(Link)
print(Number)
'''

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


'''
# The elements are organized into lazy loaded elements with data-index = "0" containing the current year and data-index = "1" containing the year prior
elements_list = element_conditional()

# Finding data index 0 and possibly data index 1. This is a list - so I'll have to loop through it accordingly.
div_elements = [elements.find("div", {"data-index": str(i)}) for i in elements_list]

print(div_elements)

new_soup = BeautifulSoup('', 'html.parser')
for div_el in div_elements:
    for child in div_el.contents:
        if isinstance(child, Tag):
            new_soup.append(child)

print(new_soup)

Date = []
ExtraData = []  # A list to store the additional data from the <dd> tags

elements = new_soup.find_all("dt")
for el in elements:
    if 'isodate' in el.attrs:  # Check if 'isodate' attribute exists
        date = el['isodate']
        Date.append(date)
        
        # Find the next <dd> element after this <dt>
        dd_sibling = el.find_next("dd")
        if dd_sibling:
            extra_data = dd_sibling.get_text().strip()  # Modify this based on what you need
            ExtraData.append(extra_data)

print(Date)
print(ExtraData)

'''