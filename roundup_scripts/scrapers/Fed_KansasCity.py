# Fed_KansasCity.py
# The purpose of this script is to scrape metadata from the most recent Kansas City Fed working papers,
# found at https://www.kansascityfed.org/research/research-working-papers/. This script uses xxx to do yyy.
#
# Lorae Stojanovic
#
# OpenAI's tool, ChatGPT, was used for coding assistance in this project.
# LE: 18 Jan 2024

import requests
import json
from bs4 import BeautifulSoup

def scrape():
    url = "https://www.kansascityfed.org/research/research-working-papers/research-working-paper-archive/"

    payload = {'csrfmiddlewaretoken': '',
    'archive-topics-search-input': '',
    'archive-authors-search-input': '',
    'archive-years': '2024',
    'archive-years': '2023',
    'archive-years-search-input': '',
    'sortby': 'date',
    'order': 'desc',
    'years': '2024;2023',
    'pageNumber': '1',
    'perPageCount': '10'}
    files=[]
    headers = {
      'Origin': 'https://www.kansascityfed.org',
      'Referer': 'https://www.kansascityfed.org/research/research-working-papers/research-working-paper-archive/',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    # Make a post request to extract a link to the landing page and get paper titles
    response = requests.request("POST", url, headers=headers, data=payload, files=files).json()
    html_content = response['rows']  # Extract the HTML content from the 'rows' key

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Initialize lists
    Title = []
    Link = []
    Number = []
    Author = []
    Date = []
    Abstract = []
    
    # Find all <a> tags within <h4> tags, which contain the titles
    elements = soup.find_all('h4')
    for el in elements:
        # Title
        title = el.text.strip()
        Title.append(title)
        
        # Link to landing page: We will ultimately use the DOI link, found on the landing page
        # for the "Link" entry of each source
        link_to_landing_page = "https://www.kansascityfed.org" + el.find('a')['href']
        
        # Navigate to landing page for date, abstract, authors, link, and number
        response = requests.get(link_to_landing_page, headers=headers)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        
        date = soup.find('time').get('datetime').strip()
        Date.append(date)
        
        author = soup.find('div', {'class': 'article-author'}).get_text().split('by:')[1].strip()
        Author.append(author)
        
        # abstract
        tags = soup.find_all(attrs={"data-block-key": True})
        if len(tags) >= 2:
            abstract = tags[1].get_text(strip=True)
        else:
            abstract = None
        Abstract.append(abstract)
                    
        # find the number. First I'll replace the previous link with this DOI link
        link = soup.find('div', {'class': 'col-12 references citations'}).find('a')['href']
        Link.append(link)
        
        # Then use the last few characters of the link to reliably procure the number
        number = link.split('RWP')[1].strip()
        Number.append(number)
        
    print(Title)
    print(Date)
    print(Author)
    print(Abstract)
    print(Link)
    print(Number)
    
        


    
    

