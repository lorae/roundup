# Fed_SanFrancisco.py
# The purpose of this script is to scrape metadata from the most recent San Francisco Fed working papers. This script uses
# the SF Fed's Working Paper landing page.
# Lorae Stojanovic
#
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 21 Aug 2023


from bs4 import BeautifulSoup
import time
from requests_html import HTMLSession
from selenium import webdriver
import pandas as pd
import requests
import re
import json

# def scrape():
# Define the URL for the SF Fed working papers API
URL = 'https://www.frbsf.org/wp-json/wp/v2/sffed_publications?publication-type=1979&per_page=10'
#URL = 'https://www.frbsf.org/wp-json/wp/v2/posts'

# Make a GET request to the SF Fed working paper API and parse the JSON response into a Python dictionary
data = json.loads(requests.get(URL).text)#['results']
print(data)

# titles = [item['title']['rendered'] for item in data]
# links = [item['link'] for item in data]
# abstracts = [item['content']['rendered'] for item in data]

# # Printing the titles
# print(titles)
# print(links)
# for abstract in abstracts:
    # print(abstract)

for item in data:
    title = item['title']['rendered']
    link = item['link']
    abstract_html = item['content']['rendered']
    authors = item['meta']['publication_authors']
    date_published = item['date'].split('T')[0]  # Extract only the date portion
    working_paper_id = item['id']
    
    # Parse the HTML abstract
    soup = BeautifulSoup(abstract_html, 'html.parser')
    abstract_text = soup.find('p').text.strip()  # Extract text from the first <p> tag
    
    # Printing details
    print("Title:", title)
    print("Link:", link)
    print("Abstract:", abstract_text)
    print("Authors:", authors)
    print("Date Published:", date_published)
    print("Working Paper ID:", working_paper_id)
    print()  # Empty line
    
    # # This page is java rendered, so we are using the requests_html package.
    # session = HTMLSession()
    
    # print(f"Scraping {url}")

    # # Send a GET request and render the JavaScript
    # r = session.get(url)
    # r.html.render(sleep=5, keep_page=True, scrolldown=1)

    # # Use BeautifulSoup to parse the page
    # soup = BeautifulSoup(r.html.html, 'html.parser')

    # # We only need the most recent 40 or so working papers... no need to get them all the way back from 2001.
    # elements = soup.find_all('article', {'class': 'cf'})[1:30]

    # # Initialize lists
    # Title = []
    # Link = []
    # Number = []
    # Author = []
    # Date = []
    # Abstract = []

    # for el in elements:
        # title = el.find('a')['title'].strip()
        # Title.append(title)
            
        # link = "https://www.frbsf.org" + el.find('a')['href']
        # Link.append(link)
        
        # number = link.split("working-papers/")[1][:-1].replace("/", "-")
        # Number.append(number)
        
        # date = el.find('meta', itemprop = 'datePublished')['content']
        # Date.append(date)
        
        # author = el.find('meta', itemprop = 'name')['content']
        # Author.append(author)
        
        # abstract = el.find('div', class_= 'collapsible').get_text().strip()
        # Abstract.append(abstract)

    # # Create a dictionary of the six lists, where the keys are the column names.
    # data = {'Title': Title,
            # 'Link': Link,
            # 'Date': Date,
            # 'Author': Author,
            # 'Number': Number,
            # 'Abstract': Abstract}

    # # Create a DataFrame from the dictionary.
    # df = pd.DataFrame(data)

    # # Instead of the data frame having row names (indices) equalling 1, 2, etc,
    # # we set them to be an identifier that is unique. In the case of Chicago, we combine
    # # Chicago with the number of the paper (eg. 999) to get an identifier Chicago999 that
    # # is completely unique across all papers scraped.
    # df["Source"] = "FED-SANFRANCISCO"
    # df.index = df["Source"] + df['Number'].astype(str)
    # df.index.name = None

    # print(df)
    # return(df)