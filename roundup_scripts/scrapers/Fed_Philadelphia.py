### Fed_Philadelphia.py ###
# The purpose of this script is to scrape metadata from the most recent Philadelphia Fed working papers. This script uses
# the Richmond Fed working paper landing page to obtain titles, links, authors and numbers. Dates and abstracts are
#  found on the specific landing pages corresponding to each individual paper. [EDIT]
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 22 Sept 2023

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from html import unescape  # Import the unescape function
import re

#all this code works but I'm commenting out for runall.py to work.
# all it needs is the date (extracted from pdf metadata?) and to be plugged in.
'''
url = "https://www.philadelphiafed.org/search-results/all-work?searchtype=working-papers"

# Get the soup for the main landing page
headers = { # imitate a browser
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
#print(soup)

# There are many <script> tags in this website's HTML, and the order in which they appear often varies. Rather than searching for the n-th <script>
# tag, I instead search for the keyword "XXX", which is unique to the script tag that contains the data we're interested in: the json-formatted data.
for script in soup.find_all('script'):
    if "Working Paper" in script.get_text():
        json_element = script
        break
#print(json_element)
# Tweak the formatting so it is legible as a JSON string. We get rid of the text before the key "data:". Then, we remove the } }) at the end of the 
# string. This gives us valid JSON.
json_str = json_element.string.split('data: ')[1].split('})')[0].strip()[:-1]
#print(json_str)
# Parse the JSON string into a Python dictionary
json_data = json.loads(json_str)

# Extract titles
# Note: unescape makes sure that characters like the apostrophe don't appear as &ldquo;, &rdquo;, and &rsquo
Title = [unescape(result['attributes']['title']) for result in json_data['results']] 
print(Title)

# Extract authors. Note that each paper has a json-formatted list of authors
author_lists = [result['attributes']['authors'] for result in json_data['results']]
# Create the author strings from the author lists
Author = [', '.join([author['name'] for author in author_list]) for author_list in author_lists]
print(Author)

# Extract number. There are these <em></em> tags all over the place that need to be removed. Then I take off the "WP " part 
# and keep only the first 5 characters which remain, which contain the number.
Number = [result['attributes']['excerpt'].replace('<em></em>', '').split('WP ')[1][:5] for result in json_data['results']] 
print(Number)

# Extract links
# Note: unescape makes sure that characters like the apostrophe don't appear as &ldquo;, &rdquo;, and &rsquo
Link = ["https://www.philadelphiafed.org" + result['attributes']['url'] for result in json_data['results']] 
print(Link)

Abstract = []
for link in Link:
    # Now we visit the individual entry page to extract authors, abstract, and number.
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    page = requests.get(link, headers=headers) # Include headers in request
    soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content using BeautifulSoup

    # Get the abstract
    abstract_element = soup.find('div', {'class': 'article-body'})
    # Extract text from all <p> tags
    p_tags = abstract_element.find_all('p')
    abstract = ' '.join(p.text for p in p_tags).strip().replace("\n", "")
    Abstract.append(abstract)

print(Abstract)

'''