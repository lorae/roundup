### ECB.py ###
# The purpose of this script is to scrape metadata from the most recent ECB working papers. This script uses
# the ECB website.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 30 August 2023

from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime

def get_soup(url): 
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    # Go to the page
    driver.get(url)
    
    time.sleep(10)

    # Get the page source and parse it
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Don't forget to close the driver
    driver.quit()

    return soup
    
url = "https://www.ecb.europa.eu/pub/research/working-papers/html/index.en.html"

soup = get_soup(url)

elements = soup.find('dl', {'class': 'ecb-basicList wpSeries ecb-lazyload pub-list-filter'})

# the element is organized into lazy loaded elements with data-index = "0" containing the current year and data-index = "1" containing the year prior
# we want an if statement here
elements = elements.find("div", {"data-index": "0"})


# Get the current month
current_month = datetime.now().strftime('%B')

# Initialize an empty list to store the elements
elements_list = []

# Check if the current month is January
if current_month == 'January':
    # Find elements where "data-index" is "0" or "1"
    elements_0 = soup.find("div", {"data-index": "0"})
    elements_1 = soup.find("div", {"data-index": "1"})
    
    # Add them to the list
    if elements_0:
        elements_list.append(elements_0)
    if elements_1:
        elements_list.append(elements_1)
else:
    # Find element where "data-index" is "0"
    elements_0 = soup.find("div", {"data-index": "0"})
    
    # Add it to the list
    if elements_0:
        elements_list.append(elements_0)

# Now, elements_list contains the elements you're interested in
for element in elements_list:
    print(element.text)

print(elements)