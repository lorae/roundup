# Fed_Dallas.py
# The purpose of this script is to scrape metadata from the most recent Cleveland Fed working papers. This script uses
# the Cleveland Fed's Working Paper landing page.
#
# Note from Lorae: This webpage is awesome. If you just scrape the url below, it gives you every single working paper
# ever published. Yes, it is dynamically rendered using Java - but all the underlying data is obtainable with one, 
# simple scrape. My favorite webpage so far to scrape.

# Never mind. Note for future self:
# webpage has groups of empty <div> tags that separate each entry.
# each set of <div> tags has an <h3> and then USUALLY 3 <p> entries under it
# <h3> contains the number
# first <p> contains title, link (to the pdf, not landing page), and abstract
# second ,p. contains more crap
# more crap
# last p contains the doi (which I want instead of the href on the title)
#
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 4 Aug 2023

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_soup(url): # Used to get the initial soup from the main URL that lists all the papers
    # In order for the code to run, it is necessary to spoof a browser. Otherwise, the website will not provide the information
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    page = requests.get(url, headers=headers) # Include headers in request
    soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content using BeautifulSoup
    return soup

url = "https://www.dallasfed.org/research/papers"

soup = get_soup(url)






# Old stuff
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_soup(url): # Used to get the initial soup from the main URL that lists all the papers
    # In order for the code to run, it is necessary to spoof a browser. Otherwise, the website will not provide the information
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    page = requests.get(url, headers=headers) # Include headers in request
    soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content using BeautifulSoup
    return soup

url = "https://www.dallasfed.org/research/papers"

soup = get_soup(url)


# Choosing elements. Filtering for all p elements first. Then we only choose those p elements
# that contain a elements with the "target" attribute equal to "_blank". But even that isn't enough
# to filter out all the gobbledygook elements (like the "Find us on Indeed.com!" and "Discount 
# Window" stuff). I finally filter things that only contain the "strong" tag, leaving only a list
# of elements that represent working papers. 
all_elements = soup.find_all('p')
special_elements = [ele for ele in elements if ele.find('a', {"target": "_blank"}) is not None]
special_elements = [ele for ele in elements if ele.find('strong') is not None][1:20]
# finally I keep only elements with 3 strong tags because there are some from pre-2001 that only
# have 2 or fewer and they mess up the code. They don't have abstracts, anyway.
#elements = [ele for ele in elements if len(ele.find_all('strong')) >= 4]
print(elements)

Title = []
Link = []
Date = []
Abstract = []
Number = []
Author = []

for el in all_elements:
    # Exception clause
    exception = False
    if el.find_all('strong')[1].get_text().strip() == "Appendix":
        exception = True
    
    # Title
    title = el.find('a').get_text()
    print(title)
    Title.append(title)
    
    # Link

    # This is a link to the pdf. But DOI is better - it has a landing page -
    # so we use that instead.
    link = "https://www.dallasfed.org" + el.find('a')['href']
    print(link)
    
    #Author and abstract
    if exception == False:
        author = el.find_all('strong')[1].get_text().strip() # The author is always the 1st strong element
        abstract = el.find_all('strong')[2].next_sibling#.strip() # The abstract is always the element after the 2nd strong
    else:
        author = el.find_all('strong')[2].get_text().strip() # Except when it is 2nd
        abstract = el.find_all('strong')[3].next_sibling.strip() # Except when it is after the 3rd strong
    print(author)
    print(".............")
    print(abstract)
    print("next==================")
    print(" ")
    
'''