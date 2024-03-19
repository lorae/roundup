# Fed_Minneapolis.py
# The purpose of this script is to scrape metadata from the most recent Minneapolis Fed working papers,
# found at https://www.minneapolisfed.org/economic-research/working-papers. This script uses xxx to do yyy.
#

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_soup(url):
    # Note that they are tricky at BEA. I have to keep changing the headers.
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
           'AppleWebKit/537.36 (KHTML, like Gecko) '\
           'Chrome/75.0.3770.80 Safari/537.36'}
           
    # Create a session
    session = requests.Session()  
    
    page = session.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup
    
# Define the URL
url = "https://www.minneapolisfed.org/economic-research/working-papers"

# Get the soup
soup = get_soup(url)
#print(soup)

# Find all the elements matching the given XPath
elements = soup.select('.i9-c-related-content__group--item')
#print(elements)

data = []
for element in elements[:2]:
    title_element = element.select_one('.i9-c-related-content__group--title')
    number_element = element.select_one('.i9-c-related-content__group--date')
    
    title = title_element.text.strip()
    print(title)
    number = number_element.text.split('Working Paper ')[1].split('(')[0].strip()
    print(number)
    link = 'https://www.minneapolisfed.org' + title_element['href']
    print(link)

    data.append({
        'Title': title,
        'Number': number_element.text.strip(),
        'Link': title_element['href']
    })

    # Access each individual WP landing page to get specific publication dates,
    # abstracts, and authors
    soup = get_soup(link)
    
    # Extract the date
    date = soup.select_one('.i9-c-title-banner__title--date').text.split('Published')[1].strip()
    print(date)

    # Extract the abstract
    # Since BeautifulSoup might correct the nested <p> tags, we target the class that uniquely identifies the text you're interested in
    abstract = soup.find("p", class_="i9-e-p__large i9-js-markdown").text.strip()
    print(abstract)

    # Extract the authors by selecting each element, and turning into a list.
    author_divs = soup.find_all("div", class_="i9-c-person-block--small__content--name")
    authors = []
    for div in author_divs:
        author_name = div.find('a').text.strip() 
        authors.append(author_name)
    # Un-list the authors into a text string separated by commas
    authors = ', '.join(authors)
    print(authors)

    print(' ')
