# Fed_Dallas.py
# The purpose of this script is to scrape metadata from the most recent Cleveland Fed working papers. This script uses
# the Cleveland Fed's Working Paper landing page.
#
# This code is still buggy. It doesn't always get a clean cut of the abstract or the authors for entries where there is
# only one p tag (typically it is a revision of a previous paper).
#
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 4 Aug 2023

import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import re

def get_soup(url): # Used to get the initial soup from the main URL that lists all the papers
    # In order for the code to run, it is necessary to spoof a browser. Otherwise, the website will not provide the information
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    page = requests.get(url, headers=headers) # Include headers in request
    soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content using BeautifulSoup
    # Find all comment tags
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))

    # Remove all comment tags from the soup
    for comment in comments:
        comment.extract()
    return soup

url = "https://www.dallasfed.org/research/papers"

soup = get_soup(url)

# First, find all the h3 tags
h3_tags = soup.find_all('h3')

count = 0
for h3 in h3_tags:
    # Stop processing if we have already processed 20 entries
    if count >= 100:
        break

    # Get the number from the h3 tag
    number = h3.text
    # Check if 'Globalization Institute' is in the number string. Replace with "GI"
    if 'Globalization Institute' in number:
        number = number.replace('Globalization Institute No. ', 'GI')
    print(number)
    
    # Navigate to the next p tag
    next_p = h3.find_next_sibling('p')
    # Get the title, abstract, and authors
    title = next_p.find('strong').text if next_p.find('strong') else None
    print(title)
    # There's many ways to get the abstract but I find splicing the string is the simplest,
    # easiest strategy in this situation.
    abstract = next_p.text.split("Abstract:")[1].strip() #everything appearing after "Abstract:" is the abstract
    abstract = abstract.split("DOI")[0].strip() # cut off anything containing a DOI
    print(abstract)
    print(":)")
    # The authors always appear after the title and before the "Abstract: " string. But sometimes,
    # there is also an "Appendix" string that has to be stripped away.
    author = next_p.text.split("Abstract:")[0].replace(title, "")
    author = author.replace("Appendix", "").replace("Code", "").strip()
    print(author)
    
    # Navigate to the last p tag before the next div tag.
    # Find the next div tag anywhere in the document after the h3 tag.
    next_div = h3.find_next('div')
    if next_div is None:
        print("doi not found")
    else:
        last_p = next_div.find_previous('p')
        doi_string = last_p.get_text()
    
    # If there only happens to be one p tag, we remove the abstract
    # to prevent confusion or duplicate information.
    if last_p == next_p:
        doi_string = last_p.get_text().replace(abstract, "")
        
    # This regular expression pattern should match most DOIs
    doi_pattern = r"(^|\n)DOI:\s*https://doi\.org/\S+"
    match = re.search(doi_pattern, doi_string)
    if match:
        link = match.group(0).replace("DOI:", "").strip()
    else:
        link = "DOI not found"
    print(link)
    
    print(".............")
    print(" ")
        
    count += 1


'''
        print(title)
    # Now we'll loop through the siblings of the h3 tag (i.e., the tags that follow it at the same level)
    for sibling in h3.find_next_siblings():
        print(h3.find_next_siblings())
        if sibling.name == 'p':
            # This is one of the p tags we're interested in
            # This is the first p tag, containing the title, link, and abstract
            title = sibling.find('strong').text if sibling.find('strong') else None
            #link = sibling.find('a')['href'] if sibling.find('a') else None
            abstract = sibling.text  # Or use any other method if the text is structured differently
            
            print(title)
            #print(link)
            print(abstract)
            print(".............")
            print(" ")
            
        elif sibling.name == 'div':
            # This is a div tag, signifying the end of the current entry
            # Increase the count and break the inner loop
            count += 1
            break

    

    # Initialize some variables to store the title, link, abstract, and DOI
    title = link = abstract = doi = None

    # Now we'll loop through the siblings of the h3 tag (i.e., the tags that follow it at the same level)
    for sibling in h3.find_next_siblings():
        if sibling.name == 'p':
            # This is one of the p tags we're interested in

            if title is None:
                # This is the first p tag, containing the title, link, and abstract
                title = sibling.find('strong').text if sibling.find('strong') else None
                link = sibling.find('a')['href'] if sibling.find('a') else None
                abstract = sibling.text  # Or use any other method if the text is structured differently

            elif 'DOI' in sibling.text:
                # This is the last p tag, containing the DOI
                doi = sibling.text  # Or use any other method if the text is structured differently

        elif sibling.name == 'div':
            # This is a div tag, signifying the end of the current entry
            break

    # Now you can do what you want with paper_number, title, link, abstract, and doi
'''



# Old stuff
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_soup(url): # Used to get the initial soup from the main URL that lists all the papers
    # In order for the code to run, it is necessary to spoof a browser. Otherwise, the website will not provide the information
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
    page = requests.get(url, headers=headers) # Include headers in request
    soup = BeautifulSoup(page.content, 'html.parser') # Parse the HTML content using BeautifulSoup
    return soup

url = "https://www.dallasfed.org/research/papers"

soup = get_soup(url)


# Choosing elements. Filtering for all p elements first. Then we only choose those p elements
# that contain a elements with the "target" attribute equal to "_blank". But even that isn't enough
# to filter out all the gobbledygook elements (like the "Find us on Indeed.com!" and "Discount 
# Window" stuff). I finally filter things that only contain the "strong" tag, leaving only a list
# of elements that represent working papers. 
all_elements = soup.find_all('p')
special_elements = [ele for ele in elements if ele.find('a', {"target": "_blank"}) is not None]
special_elements = [ele for ele in elements if ele.find('strong') is not None][1:20]
# finally I keep only elements with 3 strong tags because there are some from pre-2001 that only
# have 2 or fewer and they mess up the code. They don't have abstracts, anyway.
#elements = [ele for ele in elements if len(ele.find_all('strong')) >= 4]
print(elements)

Title = []
Link = []
Date = []
Abstract = []
Number = []
Author = []

for el in all_elements:
    # Exception clause
    exception = False
    if el.find_all('strong')[1].get_text().strip() == "Appendix":
        exception = True
    
    # Title
    title = el.find('a').get_text()
    print(title)
    Title.append(title)
    
    # Link

    # This is a link to the pdf. But DOI is better - it has a landing page -
    # so we use that instead.
    link = "https://www.dallasfed.org" + el.find('a')['href']
    print(link)
    
    #Author and abstract
    if exception == False:
        author = el.find_all('strong')[1].get_text().strip() # The author is always the 1st strong element
        abstract = el.find_all('strong')[2].next_sibling#.strip() # The abstract is always the element after the 2nd strong
    else:
        author = el.find_all('strong')[2].get_text().strip() # Except when it is 2nd
        abstract = el.find_all('strong')[3].next_sibling.strip() # Except when it is after the 3rd strong
    print(author)
    print(".............")
    print(abstract)
    print("next==================")
    print(" ")
    
'''