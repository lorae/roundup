# Fed_Minneapolis.py
# The purpose of this script is to scrape metadata from the most recent Minneapolis Fed working papers,
# found at https://www.minneapolisfed.org/economic-research/working-papers. This script uses xxx to do yyy.
# Note: This script does not distinguish between scripts that are first published and those that have been
# revised. It simply gathers both. The step where this happens is when the "date" entry is gathered. The 
# element containing the date is either split using the term "Published" or "Revised" without distinguishing
# between the two.

import requests
from bs4 import BeautifulSoup
import re
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

def scrape():   
    # Define the URL
    url = "https://www.minneapolisfed.org/economic-research/working-papers"

    # Get the soup
    soup = get_soup(url)

    # Extract the containing data on the working papers
    elements = soup.select('.i9-c-related-content__group--item')

    data = []
    # Only use the most recent 10 elements: There are many, many going back to the 
    # 1970s, and parsing through them all is unnecessary. They appear to publish 
    # infrequently, so 10 entries seems ample.
    for element in elements[:10]:
        title_element = element.select_one('.i9-c-related-content__group--title')
        number_element = element.select_one('.i9-c-related-content__group--date')
        
        # Extract title, number, and link from main landing page
        title = title_element.text.strip()
        number = number_element.text.split('Working Paper ')[1].split('(')[0].strip()
        link = 'https://www.minneapolisfed.org' + title_element['href']

        ### Access each individual WP landing page to get specific publication dates,
        ### abstracts, and authors
        soup = get_soup(link)

        # Extract the date. Note that the string is either split by the word "Published" or the word
        # "Revised" - which ever applies.
        date_text = soup.select_one('.i9-c-title-banner__title--date').text
        # Use a regular expression to split the string on either "Published" or "Revised"
        # The pattern 'Published|Revised' tells the split function to match either "Published" or "Revised"
        split_date = re.split('Published|Revised', date_text)
        # Check if the split operation found a match and returned more than one element
        if len(split_date) > 1:
            date = split_date[1].strip()  # Take the part after "Published" or "Revised" and strip whitespace
        else:
            date = None  # or some default value, depending on how you want to handle cases without these keywords
        
        ## Extract the abstract
        abstract = soup.find("p", class_="i9-e-p__large i9-js-markdown").text.strip()
        
        ## Extract the authors by selecting each element, and turning into a list.
        author_divs = soup.find_all("div", class_="i9-c-person-block--small__content--name")
        authors = []
        for div in author_divs:
            author_name = div.find('a').text.strip() 
            authors.append(author_name)
        # Un-list the authors into a text string separated by commas
        author = ', '.join(authors)

        # Add each new data point to a data dictionary
        data.append({
            'Title': title,
            'Number': number,
            'Link': link,
            'Date': date,
            'Abstract': abstract,
            'Author': author
        })

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data)

    # Instead of the data frame having row names (indices) equalling 1, 2, etc,
    # we set them to be an identifier that is unique. In the case of Chicago, we combine
    # Chicago with the number of the paper (eg. 999) to get an identifier Chicago999 that
    # is completely unique across all papers scraped.
    df["Source"] = "FED-MINNEAPOLIS"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None

    print(df)
    return(df)