# Fed_Dallas.py
# The purpose of this script is to scrape metadata from the most recent Cleveland Fed working papers. This script uses
# the Cleveland Fed's Working Paper landing page.
#
# This code is not clean. It works, but it is the worst code in this project so far. 
# In the future, the best way to improve it may be to extract the abstract from the PDF, instead of from the webpage.
# Because of the irregular formatting of elements (elements corresponding with the same working paper are rarely parent-children
# and sometimes aren't even siblings), the data is very difficult to scrape. 
# The dates are extracted from a PDF. But sometimes it reads unnecessary line breaks or spaces, which foil the regex
# formula designed to recognize dates.
#
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 7 Aug 2023

import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import re
import PyPDF2
import io

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
    
def extract_date(text):
    # Remove line breaks
    cleaned_text = text.replace('\n', ' ')

    # Regex pattern to find the date
    date_pattern = re.compile(r'(?P<month>January|February|March|April|May|June|July|August|September|October|November|December)( \d{1,2},)? \d{4}')
    match = date_pattern.search(cleaned_text)

    if match:
        return match.group()
    else:
        return None


url = "https://www.dallasfed.org/research/papers"

soup = get_soup(url)

# First, find all the h3 tags
h3_tags = soup.find_all('h3')

Title = []
Link = []
Date = []
Abstract = []
Number = []
Author = []

count = 0
for h3 in h3_tags:
    # Stop processing if we have already processed 20 entries
    if count >= 30:
        break
    
    # Get the number from the h3 tag
    number = h3.text
    # Check if 'Globalization Institute' is in the number string. Replace with "GI"
    if 'Globalization Institute' in number:
        number = number.replace('Globalization Institute No. ', 'GI')
    print(number)
    Number.append(number)
    
    # get the title from the next p tag
    next_p = h3.find_next_sibling('p')
    title = next_p.find('strong').text if next_p.find('strong') else None
    print(title)
    Title.append(title)
    # Get the link.
    # This is a link to the pdf. There are inconsistent landing pages.
    link = "https://www.dallasfed.org" + next_p.find('a')['href']
    print(link)
    Link.append(link)
    
    # get the author. It's complicated.
    # 1. Convert the p tag's contents to a string and find the location where "Abstract:" appears.
    abstract_location = str(next_p).find('Abstract:')
    # 2. Extract the substring that precedes "Abstract:".
    html_before_abstract = str(next_p)[:abstract_location]
    # 3. Parse the extracted substring using BeautifulSoup.
    soup_fragment = BeautifulSoup(html_before_abstract, 'html.parser')
    # 4. Find the last a tag within this fragment.
    last_a_tag = soup_fragment.find_all('a')[-1]
    # 5. In the original p tag, find the <br> tag right after the last a tag.
    br_tag_after_last_a = last_a_tag.find_next('br')
    # 6. Find the <strong> tag right after the <br> tag.
    author_tag = br_tag_after_last_a.find_next('strong')
    # 7. Extract the text.
    author = author_tag.text
    print(author)
    Author.append(author)
    
    print(" ")
    # get the abstract. It's complicated. And with this method, we only get the part of the abstract
    # that appears in the first p tag.
    # Find the position where "Abstract:" appears in next_p's contents.
    abstract_start = str(next_p).find('Abstract:') + len('Abstract:')
    # Get the substring starting from "Abstract:".
    substring_after_abstract = str(next_p)[abstract_start:]
    # Find the position of the first line break (either <br>, <br/>, or </br>) after "Abstract:" in the substring.
    match = re.search(r'<br ?/?>|</br>', substring_after_abstract)
    if match:
        abstract_end = match.start()
    else:
        abstract_end = len(substring_after_abstract)  # if no match found, use the full length
    #abstract_end = substring_after_abstract.find('<br>')
    # Extract the desired abstract text.
    abstract_html = substring_after_abstract[:abstract_end].strip()
    abstract_soup = BeautifulSoup(abstract_html, 'html.parser')
    abstract = abstract_soup.get_text()
    print(abstract)
    Abstract.append(abstract)
    
    print(".....")
    print(" ")
    count += 1
    
# get the date frim PDF file. Complicated.
#Link = ["https://www.dallasfed.org/-/media/documents/research/papers/2023/wp2305.pdf"]
# The extract_date function doesn't always work because sometimes the text has weird spaces and line breaks
# that mess up the regex (e.g. "M ay 5, 2023" instead of "May 5, 2023"). I'd like to also extract the abstract
# from the PDF but I need to learn how to remove the unnecessary line breaks and spaces first. The above link
# is an example of a PDF that produces this error.
for link in Link:
    # Get the PDF content for the current row
    pdf_content = requests.get(link).content
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    
    # Extract the text from the second page
    text = pdf_reader.pages[1].extract_text().replace('\n', ' ')
    #print(text)
    date = extract_date(text)
    print(date)
    

    


'''
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
    
    # Remove all the links that follow the abstract
    for link in next_p.find_all('a'):
        abstract = abstract.replace(link.text, '').strip()
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