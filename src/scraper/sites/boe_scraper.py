from src.scraper.get_soup import get_soup
import feedparser
import requests
import pandas as pd
from ..generic_scraper import GenericScraper

class BOEScraper(GenericScraper):
    def __init__(self):
        # assigning the `source` attribute in the superclass to 'BOE'
        super().__init__('BOE')
        # Define headers once and use them throughout the class
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }


    # Public method which is called from outside the class.
    def collect_data(self):
        # Request and parse RSS feed contents
        url = "https://www.bankofengland.co.uk/rss/publications"
        f = feedparser.parse(url)

        # Cycle through RSS feed entries for working papers, and extract titles, links, and dates
        data = []
        for entry in f.entries:
            if "working paper" in entry.summary:
                # Collect data from the RSS feed
                title = entry.title
                link = entry.link
                date = entry.published[:-14]

                # Visit the landing page for each working paper to extract the remaining data.
                # Bundle the arguments together for requests module
                session_arguments = requests.Request(method='GET', url=entry.link, headers=self.headers)
                # Send request and get soup from landing page
                soup = get_soup(session_arguments)
                
                # Extract remaining data on abstract, authors, number from landing page soup
                abstract = self.get_abstract(soup)
                authors = self.get_authors(soup)
                number = self.get_number(soup)
                                
                # Append this data to `data`
                data.append({
                    'Title': title,
                    'Link': link,
                    'Date': date,
                    'Abstract': abstract,
                    'Author': authors,
                    'Number': number       
                })
            else:
                # skip to the next iteration of the for loop. Do not log data for this entry
                continue

        # Use the inherited process_data method to create and return the DataFrame
        return self.process_data(data)

    # Private method used to get abstract
    def get_abstract(self, soup):
        abstract_tags = soup.find('div', {'class': 'page-content'}).find_all(['p', 'div'], recursive=False)

        potential_abstracts = []
        for tag in abstract_tags:
            # Check if this is the download button. The abstract always appears before the download button on the webpage
            if tag.find('a', {'class': 'btn btn-pubs btn-has-img btn-lg'}):
                break
            potential_abstracts.append(tag.text.strip())
        
        # Choose the longest potential abstract and remove the leading and trailing character (which is a [ and ])
        abstract = max(potential_abstracts, key=len) if potential_abstracts else None

        return abstract
    
    # Private method used to get authors
    def get_authors(self, soup):
        authors = (soup.find('div', {'class': 'page-content'})  # Find the 'div' tag with class 'page-content'
            .text # Extract the text of the 'div' tag
            .strip() # Remove any leading/trailing whitespace from the text
            .split('\n')[1] # Split the text by newline character '\n' and return the first element
            .replace('By', '') # Remove unnecessary text
            .strip()) # Remove any leading/trailing whitespace from the text
        
        return authors
    
    # Private method to get number
    def get_number(self, soup):
        number = (soup.find('div', {'class': 'page-content'})  # Find the 'div' tag with class 'page-content'
            .text # Extract the text of the 'div' tag
            .strip() # Remove any leading/trailing whitespace from the text
            .split('\n')[0] # Split the text by newline character '\n' and return the zero-th element
            .replace('Staff Working Paper No.', '') # remove unnecessary text
            .replace(',', '') # remove unnecessary commas
            .strip()) # Remove any leading/trailing whitespace from the text
        
        return number

       