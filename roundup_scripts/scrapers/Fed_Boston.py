# Fed_Boston.py
# The purpose of this script is to scrape metadata from the most recent Boston Fed working papers. This script uses
# the Boston Fed's Working Paper landing page.
# Lorae Stojanovic
#
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 21 Aug 2023

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import PyPDF2
from io import BytesIO
from datetime import datetime
import pandas as pd

def get_soup(url): 
    chrome_service = Service(ChromeDriverManager().install())
    
    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]
    for option in options:
        chrome_options.add_argument(option)

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Go to the page
    driver.get(url)

    # Wait for the button with the specific aria-label and then click it
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="2023 Series"]'))
    )
    button.click()

    # Wait until a certain number of 'event-list-item' divs appear. Adjust the number '10' as needed.
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'event-list-item'))
    )
    time.sleep(5)

    # Get the page source and parse it
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Don't forget to close the driver
    driver.quit()

    return soup
    
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
    url = "https://www.bostonfed.org/publications/research-department-working-paper/"
    soup = get_soup(url)
    #print(soup)

    elements = soup.find('div', {'class': 'event-list'}).find_all('div', {'class': 'event-body-wrapper'})
    #print(elements)

    # Initialize lists
    Title = []
    Link = []
    Number = []
    Author = []
    Date = []
    Abstract = []


    for el in elements:
        # Getting the title from the landing page
        title = el.find('h2', {'class': 'card-title'}).find('a')['title'].strip()
        Title.append(title)
        
        # Getting the link from the landing page
        link = "https://www.bostonfed.org" + el.find('h2', {'class': 'card-title'}).find('a')['href']
        Link.append(link)
        
        # Now we visit the individual entry page to extract authors, abstract, and number.
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
        page = requests.get(link, headers=headers) # Include headers in request
        soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content using BeautifulSoup
        
        # Getting the authors from the individual WP page
        author = soup.find('div', {'class': 'row working-paper-by-author-row'}).get_text().strip().replace("By ", "")
        Author.append(author)
        
        # Getting the abstract from the individual WP page
        abstract = soup.find('div', {'id': 'collapse3'}).get_text().strip()
        Abstract.append(abstract)
        
        # Getting the number from the individual WP page
        number = soup.find('p', {'class': 'doi-text'}).get_text().split("No. ")[1].split("https:")[0].replace(".", "").strip()
        Number.append(number)
        
        # Now we use the PDF metadata to get the date
        # But first, we need the link to the pdf.
        pdf_link = "https://www.bostonfed.org" + soup.find('div', {'class': 'row working-paper-download-bttn-row'}).find('a', {'role': 'button'})['href']
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
    df["Source"] = "FED-BOSTON"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None

    print(df)
    return(df)