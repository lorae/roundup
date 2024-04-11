from ..generic_scraper import GenericScraper
from src.scraper.get_soup import request_soup
import requests
import re

class FedStLouisScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'FED-STLOUIS')
        # Define generic headers to be used later in the class
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

    def fetch_data(self):
        url = 'https://research.stlouisfed.org/wp/'
        # Bundle the arguments together for requests module
        session_arguments = requests.Request(method='GET', 
                                             url=url, 
                                             headers=self.headers)
        # Send request and parse soup using BeautifulSoup
        soup = request_soup(session_arguments)
        # The misspelling of "seperator" is faithful to the website
        elements = soup.select('div.seperator-bottom') 

        
        # Initialize `data`
        data = []
        for el in elements:
            # Title
            title = el.find('a', {'class': 'title'}).text.strip()
            
            # Link
            link = ('https://research.stlouisfed.org/' 
                    + el.find('a', {'class': 'title'})['href'])
            
            # Author
            author_text = el.find('span', {'class': 'byline'}).text
            author_text = author_text.split("Working Paper")[0]  # Keep the part before "Working Paper"
            author_text = author_text.replace("\n", " ")  # Replace newlines with spaces
            author_text = re.sub(' +', ' ', author_text)  # Replace multiple spaces with a single space
            author_text = re.sub('by', "", author_text)  # Remove the word "by" 
            author_text = author_text.strip()  # Remove leading and trailing spaces
            author = author_text
            
            # Number
            number_text = el.find('span', {'class': 'byline'}).text
            number_text = number_text.split("Working Paper")[1]  # Keep the part after "Working Paper"
            number_text = number_text.split("updated")[0]  # Keep the part before "updated"
            number_text = number_text.split("added")[0]  # Keep the part before "added"
            number_text = number_text.strip()  # Remove leading and trailing spaces
            number = number_text
            
            # Date
            date_text = el.find('span', {'class': 'byline'}).text
            date_text = date_text.split(f'{number}')[1]  # Keep the part after the working paper number
            date_text = re.sub('updated', '', date_text) # Remove "updated"
            date_text = re.sub('added', '', date_text) # Remove "added"
            date_text = date_text.strip()  # Remove leading and trailing spaces
            date = date_text
            
            # Abstract
            abstract = el.find_all('p')[1].text.strip()

            # Append title, link, author, number, date, and abstract
            # to `data`
            data.append({
                'Title': title,
                'Link': link,
                'Author': author,
                'Number': number,
                'Date': date,
                'Abstract': abstract
            })

        return data