from ..generic_scraper import GenericScraper
from src.scraper.external_requests import request_soup
import requests

class FedRichmondScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = "FED-RICHMOND")
        # Define headers once and use them throughout the class
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }
    

    # Public method which is called from outside the class.
    def fetch_data(self):
        '''
        Sends a GET request to the source's main page and parses the 
        response using BeautifulSoup to get title, link, author, date,
        and number for each working paper entry. 
        A secondary GET request is made to each working paper's 
        landing page and parsed using BeautifulSoup to extract working 
        paper abstracts.

        :return: A list of dictionaries containing Title, Author, Link, 
        Abstract, Number and Date for each working paper entry 
        :rtype: list
        '''
        url = 'https://www.richmondfed.org/publications/research/working_papers'
        # Bundle the arguments together for requests module
        session_arguments = requests.Request(method='GET', 
                                             url=url, 
                                             headers=self.headers)
        # Send request and parse soup using BeautifulSoup
        soup = request_soup(session_arguments)
        elements = soup.find_all('div', {'class': 'data__row'})

        # Initialize `data`
        data = []
        for el in elements:
            # Title
            title = el.find('div', {'class': 'data__title'}).get_text().replace('\n', '').strip()
            
            # Author
            author = el.find('div', {'class': 'data__authors'}).get_text().replace('\n', '').strip()
            
            # Number
            number = el.find('span', {'class': 'data__issue'}).get_text().split('No. ')[1].strip()
            
            #Link
            link = 'https://www.richmondfed.org' + el.find('div', {'class': 'data__title'}).find('a')['href']

            # Date. This used to be gathered with more precise information
            # from the PDF for the working paper on the landing page, but the
            # code has been since simplified to use the metadata found on the 
            # main page.
            date = el.find('span', {'class': 'data__issue'}).text.split(',')[0].strip()

            # Navigate to the individual landing page to get the abstract and the date
            # Bundle the arguments together for requests module
            session_arguments = requests.Request(method='GET', 
                                                url=link, 
                                                headers=self.headers)
            # Send request and parse soup using BeautifulSoup
            landing_soup = request_soup(session_arguments)
            
            # Abstract
            abstract = landing_soup.find('div', {'class': 'working-paper__abstract'}).get_text().strip()

            # Append title, author, number, link, date, and abstract
            # to `data`
            data.append({
                'Title': title,
                'Author': author,
                'Number': number,
                'Link': link,
                'Date': date,
                'Abstract': abstract
            })

        return data