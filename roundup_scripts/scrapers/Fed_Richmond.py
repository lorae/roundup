### Fed_Richmond.py ###
# The purpose of this script is to scrape metadata from the most recent Richmond Fed working papers. This script uses
# the Richmond Fed working paper landing page to obtain titles, links, authors and numbers. Dates and abstracts are
#  found on the specific landing pages corresponding to each individual paper.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 22 Sept 2023

import requests
from bs4 import BeautifulSoup
import pandas as pd
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
    url = "https://www.richmondfed.org/publications/research/working_papers"

    # Get the soup for the main landing page
    headers = { # imitate a browser
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    elements = soup.find_all('div', {'class': 'data__row'})

    # Initialize lists
    Title = []
    Link = []
    Number = []
    Author = []
    Date = []
    Abstract = []

    for el in elements:
        # Get the title, author, number and link from the main landing page
        # Title
        title = el.find('div', {'class': 'data__title'}).get_text().replace("\n", "").strip()
        Title.append(title)
        
        # Author
        author = el.find('div', {'class': 'data__authors'}).get_text().replace("\n", "").strip()
        Author.append(author)
        
        # Number
        number = el.find('span', {'class': 'data__issue'}).get_text().split("No. ")[1].strip()
        Number.append(number)
        
        #Link
        link = "https://www.richmondfed.org/" + el.find('div', {'class': 'data__title'}).find('a')['href']
        Link.append(link)

        # Navigate to the individual landing page to get the abstract and the date
        response = requests.get(link, headers=headers)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Abstract
        abstract = soup.find('div', {'class': 'working-paper__abstract'}).get_text().strip()
        Abstract.append(abstract)

        # Date. We use the PDF metadata to get the date. But first, we need the link to the pdf.
        pdf_link = "https://www.richmondfed.org/" + soup.find('span', {'class': 'comp-icon-bar__pdf'}).find('a')['href']
        # Now we download the PDF and access its metadata using the user-defined extract_pdf_metadata_from_url function
        metadata = extract_pdf_metadata_from_url(pdf_link)
        # Now we further extract and format the date of last modification using the user-defined extract_and_format_moddate function
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
    df["Source"] = "FED-RICHMOND"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None

    print(df)
    return(df)
