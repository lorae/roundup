from src.scraper.get_soup import request_soup
from ..generic_scraper import GenericScraper
import requests


class BEAScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'BEA')
        # Define headers once and use them throughout the class
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

    # Public method which is called from outside the class. 
    def fetch_data(self):
        '''
        Sends a GET request to the source's main page and parses the 
        response using BeautifulSoup to get title, link, author, and date
        for each working paper entry. 
        A secondary GET request is made to each working paper's
        landing page and parsed using BeautifulSoup to extract
        number and abstract data.

        :return: A list of dictionaries containing Title, Author, Link, 
        Abstract, Number and Date for each working paper entry 
        :rtype: list
        '''
        url = 'https://www.bea.gov/research/papers'
        # Bundle the arguments together for requests module
        session_arguments = requests.Request(method='GET', url=url, headers=self.headers)
        # Send request and get soup
        soup = request_soup(session_arguments)
        
        elements = soup.select('div.view-content div.card')
        data = []
        for element in elements:
                # Get the link to the landing page of the working paper. Bundle request arguments and parse as soup.
                landing_url = 'https://www.bea.gov/' + element.find('h2', {'class': 'paper-title'}).find('a')['href']
                session_arguments = requests.Request(method='GET', url=landing_url, headers=self.headers)
                landing_soup = request_soup(session_arguments)

                # The number_url is the URL of a PDF on the landing page which will contain the working paper number
                number_url = landing_soup.find('h2', class_='card-title').find('a')['href'] # the URL containing the number
                # First we check if the paper is, indeed, a working paper. If it is, its url should contain "BEA-WP"
                if "BEA-WP" in number_url:
                        # Split the url to pieces before and after characters "BEA-". Keep only the piece following "BEA-" which
                        # contains the working paper number. Remove the ".pdf" at the end.
                        number = number_url.split('BEA-')[1].replace('.pdf', '')
                else:
                        # Skip to the next iteration of the for loop. Do not log data for this entry
                        continue
                # Abstract
                abstract = landing_soup.find('p', {'class': 'card-abstract'}).get_text(strip=True)
                
                # Append all the new data to a dictionary
                data.append({
                        'Title': element.find('h2', {'class': 'paper-title'}).text.strip(),
                        'Link': landing_url,
                        'Author': element.find('div', {'class': 'paper-mod-date'}).text.strip(),
                        'Date': element.find('time').get('datetime').split("T")[0],
                        'Number': number,
                        'Abstract': abstract
                })
                
        # Use the inherited process_data method to create and return the DataFrame
        return data