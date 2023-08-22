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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import PyPDF2
from io import BytesIO
import io


def get_soup(url): 
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

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
    
url = "https://www.bostonfed.org/publications/research-department-working-paper/"
soup = get_soup(url)
#print(soup)

elements = soup.find('div', {'class': 'event-list'}).find_all('div', {'class': 'event-body-wrapper'})
#print(elements)

for el in elements:
    title = el.find('h2', {'class': 'card-title'}).find('a')['title']
    print(title)
    
    link = "https://www.bostonfed.org" + el.find('h2', {'class': 'card-title'}).find('a')['href']
    print(link)
    
    # now we get the rest.
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    page = requests.get(link, headers=headers) # Include headers in request
    soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content using BeautifulSoup
    
    authors = soup.find('div', {'class': 'row working-paper-by-author-row'}).get_text().strip().replace("By ", "")
    print(authors)
    
    abstract = soup.find('div', {'id': 'collapse3'}).get_text().strip()
    print(abstract)
    
    number = soup.find('p', {'class': 'doi-text'}).get_text().split("No. ")[1].split("https:")[0].replace(".", "").strip()
    print(number)




# Example usage
pdf_url = 'https://www.bostonfed.org/-/media/Documents/Workingpapers/PDF/2023/wp2308.pdf'
metadata = extract_pdf_metadata_from_url(pdf_url)

for key, value in metadata.items():
    print(f"{key}: {value}")

from datetime import datetime

def extract_and_format_moddate(metadata):
    # Extract the ModDate string
    mod_date_str = metadata['/ModDate'][2:16]  # Extracts '20230303104258' from 'D:20230303104258-05'00''
    
    # Parse the ModDate string into a datetime object
    mod_date = datetime.strptime(mod_date_str, '%Y%m%d%H%M%S')
    
    # Format the datetime object in the desired format
    formatted_date = mod_date.strftime('%b %d, %Y')
    
    return formatted_date


formatted_mod_date = extract_and_format_moddate(metadata)
print(formatted_mod_date)  # Outputs: Mar 03, 2023

# This webpage is horrible to parse. Not working.
'''
for el in elements:
    authors = el.find('p', {'class': 'pub-card-authors'}).find_all('a', {'ng-href': True})
    for a in authors:
        author = a.get_text()
        print(author)
#elements = soup.find_all('div', {'class': 'event-list-item'})
#print(elements)
'''

