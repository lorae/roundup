# The purpose of this script is to scrape metadata from the most recent New York Fed working papers. This script uses
# the New York Fed "Staff Reports" landing page and also clicks on individual links to procure XX and YY. 
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 1 Aug 2023

import requests
from datetime import datetime

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

    # Print out the list of URLs
    print(url)
    return(url)

url_conditional(before = "https://www.newyorkfed.org/research/staff_reports/index.html#", after = "")