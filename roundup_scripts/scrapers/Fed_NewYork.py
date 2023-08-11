# Fed_NewYork.py
# The purpose of this script is to scrape metadata from the most recent New York Fed working papers. This script uses
# the New York Fed "Staff Reports" landing page and also clicks on individual links to procure abstracts. 
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 1 Aug 2023

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from requests_html import HTMLSession
import pandas as pd

# Function to check if a URL exists by checking the HTTP status code
def url_exists(url):
    response = requests.get(url)
    return response.status_code == 200

# Function to create a url list based on date conditions. It takes before and after as arguments, which are strings
# that specify the URL structure before and after the year appears. For example, in 
# "https://www.newyorkfed.org/research/staff_reports/index.html#2023"
# the before_string is "https://www.newyorkfed.org/research/staff_reports/index.html#" and the after string is
# "" (empty).
# If the current date is in Jan or Feb, it contain's this year's and last year's url (after checking that this
# year's url does indeed exist - a non-trivial question if the code is being run on Jan 1 or 2, when people may
# still be on holiday and the webpage is not up yet. If the current date is in any month from March - December,
# then this function makes a list of one url for the current year.
def url_conditional(before, after):
    # Initialize an empty list for the URLs
    url = []

    # Get the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month

    # If the current month is January or February
    if current_month in [1, 2]:
        # Create a URL for the current year
        current_year_url = f"{before}{current_year}{after}"
        
        # If the URL exists, add it to the list
        if url_exists(current_year_url):
            url.append(current_year_url)
            
        # Create a URL for the previous year and add it to the list
        last_year_url = f"{before}{current_year - 1}{after}"
        url.append(last_year_url)

    # If the current month is not January or February
    else:
        # Add a URL for the current year to the list
        url.append(f"{before}{current_year}{after}")

    return(url)



def scrape():
    # This page is java rendered, so we are using the requests_html package.
    session = HTMLSession()

    url_list = url_conditional(before = "https://www.newyorkfed.org/research/staff_reports/index.html#", after = "")

    # Initialize lists
    Title = []
    Link = []
    Number = []
    Author = []
    Date = []
    Abstract = []

    for url in url_list:
        print(f"Scraping {url}")

        # Send a GET request and render the JavaScript
        r = session.get(url)
        r.html.render(sleep=2, keep_page=True, scrolldown=1)

        # Use BeautifulSoup to parse the page
        soup = BeautifulSoup(r.html.html, 'html.parser')
        elements = soup.select('tr > td > p')

        # Filter elements based on the presence of 'a' tag (to avoid the 7 unnecessary p elements)
        elements = [el for el in elements if el.select_one('a')]

        # Append data to Title, Link, Number, Author lists
        Title += [el.select_one('a').text.strip() for el in elements]
        Link += ["https://www.newyorkfed.org" + el.select_one('a')['href'] for el in elements]
        Number += [el.select_one('a')['href'].split("/sr")[1].replace('.html', '') for el in elements]
        Author += [list(el.stripped_strings)[1] for el in elements]

        # Append to Date list. Date is slightly more complicated, so I've moved it out of the list 
        # comprehension to show it more step-by-step.
        for el in elements:
            date_raw = el.select_one('span.paraNotes').get_text().split('\xa0')
            month = date_raw[1].strip()[4:]
            year = date_raw[2].strip()
            Date.append(month + " " + year)

        # Append to Abstract list. They are located on a separate url found in Link.
        for link in Link:
            response = requests.get(link)
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')

            # Get the abstracts
            abstract = soup.select('div.ts-article-text')[1].text.strip().replace('\n', ' ')
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
    df["Source"] = "FED-NEWYORK"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None


    # Convert the set to a list and get the relevant rows from the df. Then
    # save as csv using filepath. And use utf-8 encoding to ensure special 
    # characters are captured.
    df.to_csv('test-pleasedelete.csv', encoding='utf-8')
        
        
    print(df)
    return(df)