### Fed_Philadelphia.py ###
# The purpose of this script is to scrape metadata from the most recent Philadelphia Fed working papers. This script uses
# the Philadelphia Fed working paper landing page to obtain titles, links, authors and numbers. Abstracts are found on the
# specific landing pages corresponding to each individual paper, and dates are estimated using PDF metadata.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 23 Sept 2023

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from html import unescape  # Import the unescape function
import re
import PyPDF2
from io import BytesIO
import io
from datetime import datetime

def extract_pdf_metadata_from_url(pdf_url):
    # Download the PDF
    response = requests.get(pdf_url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Use BytesIO to convert the downloaded content to a file-like object so it can be read by PyPDF2
    with BytesIO(response.content) as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract metadata
        metadata = pdf_reader.metadata

    return metadata

def extract_and_format_moddate(metadata):
    # Extract the ModDate string
    mod_date_str = metadata['/ModDate'][2:16]  # Extracts '20230303104258' from 'D:20230303104258-05'00''
    
    # Parse the ModDate string into a datetime object
    mod_date = datetime.strptime(mod_date_str, '%Y%m%d%H%M%S')
    
    # Format the datetime object in the desired format
    formatted_date = mod_date.strftime('%B %d, %Y')
    
    return formatted_date

def scrape():
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

    # Extract titles. Note: unescape makes sure that characters like the apostrophe don't appear as &ldquo;, &rdquo;, and &rsquo
    Title = [unescape(result['attributes']['title']) for result in json_data['results']] 

    # Extract authors. Note that each paper has a json-formatted list of authors
    author_lists = [result['attributes']['authors'] for result in json_data['results']]
    # Create the author strings from the author lists
    Author = [', '.join([author['name'] for author in author_list]) for author_list in author_lists]

    # Extract number. There are these <em></em> tags all over the place that need to be removed. Then I take off the "WP " part 
    # and keep only the first 5 characters which remain, which contain the number.
    Number = [result['attributes']['excerpt'].replace('<em></em>', '').split('WP ')[1][:5] for result in json_data['results']] 

    # Extract links.
    Link = ["https://www.philadelphiafed.org" + result['attributes']['url'] for result in json_data['results']] 

    # Initialize lists for abstract and date
    Abstract = []
    Date = []

    for link in Link:
        # Visit the individual entry page abstract and date
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
        page = requests.get(link, headers=headers) # Include headers in request
        soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content using BeautifulSoup

        # Extract abstract
        abstract_element = soup.find('div', {'class': 'article-body'})
        # Extract text from all <p> tags
        p_tags = abstract_element.find_all('p')
        abstract = ' '.join(p.text for p in p_tags).strip().replace("\n", "")
        Abstract.append(abstract)

        # Extract date. We use the PDF metadata to get the date. But first, we need the link to the pdf.
        pdf_link = "https://www.philadelphiafed.org" + soup.find('li', {'class': 'share-download circle-icon show-pdf'}).find('a')['href']
        # Now we download the PDF and access its metadata using the user-defined extract_pdf_metadata_from_url function
        metadata = extract_pdf_metadata_from_url(pdf_link)
        # Now we further extract and format the date of last modification
        date = extract_and_format_moddate(metadata)
        Date.append(date)

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
    df["Source"] = "FED-PHILADELPHIA"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None

    print(df)
    return(df)