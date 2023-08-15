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

url = "https://www.frbsf.org/economic-research/publications/working-papers/"

# Get the soup
soup = get_soup(url)

#print(soup)

# We only need the most recent 50 or so working papers... no need to get them all the way back from 2001.
elements = soup.find_all('article', {'class': 'cf'})[1:10]

print(elements)

# Initialize lists
Title = []
Link = []
Number = []
Author = []
Date = []
Abstract = []

for el in elements:
    title = el.find('a')['title'].strip()
    print(title)
    
    link = "https://www.frbsf.org" + el.find('a')['href']
    print(link)
    
    number = link.split("working-papers/")[1][:-1].replace("/", "-")
    print(number)