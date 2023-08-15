# Fed_Boston.py
# The purpose of this script is to scrape metadata from the most recent Boston Fed working papers. This script uses
# the Boston Fed's Working Paper landing page.
# Lorae Stojanovic
#
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 15 Aug 2023

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd

def get_soup(url): # Used to get the initial soup from the main URL that lists all the papers
    # In order for the code to run, it is necessary to spoof a browser. Otherwise, the website will not provide the information
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    page = requests.get(url, headers=headers) # Include headers in request
    soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content using BeautifulSoup
    return soup
    
    
 
url = "https://www.bostonfed.org/publications/research-department-working-paper/"
soup = get_soup(url)
print(soup)