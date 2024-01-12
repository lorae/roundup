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
import json

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

    url_list = url_conditional(before = "https://www.newyorkfed.org//api/research/getsritemshtml?year=", after = "&useLucene=true")

    # Initialize lists
    Title = []
    Link = []
    Number = []
    Author = []
    Date = []
    Abstract = []

    for url in url_list:
        print(f"Scraping {url}")
        
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            continue  # Skip to the next iteration of the parent for loop
        
        for entry in data:
            # AUTHOR: Assign the value of 'AuthorsHtml' or 'No authors listed' if 'AuthorsHtml' is missing or empty
            Author += [entry.get("AuthorsHtml").strip() or "No authors listed"]
            # TITLE:
            Title += [entry.get("Paper_Title").strip() or "No title listed"]   
            # DATE:
            Date += [entry.get("PublicationDate", "No publication date listed")]
            # LINK: Assigning link a variable name so it can be used in logical sequences below
            link = "https://www.newyorkfed.org/" + entry.get("Uri") or "No link listed" # will have to find a way to put an error in
            Link += [link]
            # NUMBER: Series of logical steps to get number entry. Number is essential because it is used to uniquely identify
            # papers. Thus, we try to use several unique identifiers as a number before ultimately quitting the script
            # if none are successful.
            # 1) Attempt to assign 'Series_Number' or fallback to "No series number listed"
            number = entry.get("Series_Number", "").strip() or "No series number listed"
            if number == "No series number listed":
                # 2) If Series_Number not listed, check if link is present. If link present (defined above), extract the last 4 characters 
                # as the number
                if link != "No link listed":
                    number = link[-4:].strip()
                else:
                    # 3) If no link, try to use 'Id'
                    id_number = entry.get("Id") or "No ID listed"
                    if id_number != "No ID listed":
                        number = id_number
                    else:
                        # 4) If 'Id' is also not present, report a fatal error and exit
                        print("Fatal error: Unable to assign unique ID number to entry.")
                        sys.exit()
            Number += [number]
            # ABSTRACT: must visit each link to get the abstract, since it is not in the main API.
            response = requests.get(link)
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            Abstract += [soup.select('div.ts-article-text')[1].text.strip().replace('\n', ' ')]
   
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

    print(df)
    return(df)