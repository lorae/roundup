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

def scrape():
    url = "https://www.dallasfed.org/research/papers"

    soup = get_soup(url)

    Title = []
    Link = []
    Date = []
    Abstract = []
    Number = []
    Author = []

    # First, find all the h3 tags. These act as signposts that definitively separate working
    # paper entries.
    h3_tags = soup.find_all('h3')

    count = 0
    for h3 in h3_tags:
        # Stop processing if we have already processed 20 entries
        if count >= 20:
            break
        
        # NUMBER. Get the number from the h3 tag.
        number = h3.text
        # Check if 'Globalization Institute' is in the number string. Replace with "GI"
        if 'Globalization Institute' in number:
            number = number.replace('Globalization Institute No. ', 'GI')
        Number.append(number)
        
        # TITLE. Get the title from the first p tag that follows the h3 tag.
        next_p = h3.find_next_sibling('p')
        title = next_p.find('strong').text if next_p.find('strong') else None
        Title.append(title)
        # LINK. Get the link from the first p tag that follows the h3 tag. Note that this is a link to a pdf, NOT 
        # a landing page. Some working papers have landing pages, but it is inconsistent.
        link = "https://www.dallasfed.org" + next_p.find('a')['href']
        Link.append(link)
        
        # AUTHOR. The author also comes from the first p tag that follows the h3 tag. But it is 
        # complicated to extract since it doesn't have its own element. The cleanest way to extract
        # the data is to parse the element as text and then convert back to a beautiful soup to then
        # once again extract the clean text.
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
        Author.append(author)
        
        # ABSTRACT. Methodology similar to author above.
        # There's room for improvement in this code, and perhaps a better solution is using the PDF,
        # as is done for the paper date.
        # 1. Find the position where "Abstract:" appears in next_p's contents.
        abstract_start = str(next_p).find('Abstract:') + len('Abstract:')
        # 2. Get the substring starting from "Abstract:".
        substring_after_abstract = str(next_p)[abstract_start:]
        # 3. Find the position of the first line break (either <br>, <br/>, or </br>) after "Abstract:" in the substring.
        match = re.search(r'<br ?/?>|</br>', substring_after_abstract)
        if match:
            abstract_end = match.start()
        else:
            abstract_end = len(substring_after_abstract)  # if no match found, use the full length
        # 4. Extract the desired abstract text by converting back to a soup, and then again to text. This removes unneeded 
        # <p> and <br> tags and the like.
        abstract_html = substring_after_abstract[:abstract_end].strip()
        abstract_soup = BeautifulSoup(abstract_html, 'html.parser')
        abstract = abstract_soup.get_text()
        Abstract.append(abstract)
        
        # counter to ensure the loop only runs a limited number of times. Otherwise we'd extract data all the way
        # back to the 1980's (yes, seriously!)
        count += 1
        
    # get the date frim PDF file. Complicated.
    # Link = ["https://www.dallasfed.org/-/media/documents/research/papers/2023/wp2305.pdf"]
    # The extract_date function doesn't always work because sometimes the text has spaces and line breaks
    # that mess up the regex (e.g. "M ay 5, 2023" instead of "May 5, 2023"). I'd like to also extract the abstract
    # from the PDF but I need to learn how to remove the unnecessary line breaks and spaces first. The above link
    # is an example of a PDF that produces this error. Most work, however.
    for link in Link:
        # Get the PDF content for the current row
        pdf_content = requests.get(link).content
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        
        # Extract the text from the second page
        text = pdf_reader.pages[1].extract_text().replace('\n', ' ')
        #print(text)
        date = extract_date(text)
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
    df["Source"] = "FED-DALLAS"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None

    print(df)
    return(df)
        
