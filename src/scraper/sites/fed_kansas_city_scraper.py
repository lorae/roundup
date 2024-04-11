from ..generic_scraper import GenericScraper
from src.scraper.get_soup import request_json, request_soup
from datetime import datetime
from bs4 import BeautifulSoup
import requests

class FedKansasCityScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'FED-KANSAS-CITY')
        # Define generic headers to be used later in the class
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

    def fetch_data(self):
        # Get the current year
        current_year = datetime.now().year
        last_year = current_year - 1

        # Prepare the contents of the network request using dynamically
        # generated current_year and last_year. This type of current and last
        # year data request is useful in the edge case when the current date
        # is in early January and recently published papers could belong
        # have been published last year.
        url = 'https://www.kansascityfed.org/research/research-working-papers/research-working-paper-archive/'
        payload = {'csrfmiddlewaretoken': '',
        'archive-topics-search-input': '',
        'archive-authors-search-input': '',
        'archive-years': f'{current_year},{last_year}',
        'archive-years-search-input': '',
        'sortby': 'date',
        'order': 'desc',
        'years': f'{current_year},{last_year}',
        'pageNumber': '1',
        'perPageCount': '10'}
        files=[]
        main_headers = {
        'Origin': 'https://www.kansascityfed.org',
        'Referer': 'https://www.kansascityfed.org/research/research-working-papers/research-working-paper-archive/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # Make a post request and parse as json
        response = request_json(method = 'POST', 
                                url = url, 
                                headers = main_headers, 
                                data = payload, 
                                files = files)
        # Extract the HTML content from the 'rows' key
        html_content = response['rows']  
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Initialize `data`
        data = []
        # Find all <h4> tags, which contain the elements that contain relevant data
        elements = soup.find_all('h4')
        for el in elements:
            # Title
            title = el.text.strip()
            
            # Link to landing page: Used to navigate to the landing page to collect more data. This script
            # ultimately records the paper link as the DOI link, collected from the landing page later in 
            # this script.
            link_to_landing_page = "https://www.kansascityfed.org" + el.find('a')['href']
            
            # Navigate to landing page for date, abstract, authors, link, and number
            # Bundle the arguments together for requests module
            session_arguments = requests.Request(method='GET', 
                                                 url=link_to_landing_page, 
                                                 headers=self.headers)
            # Send request and get soup for landing page
            landing_soup = request_soup(session_arguments)
            
            # Date (from landing page)
            date = landing_soup.find('time').get('datetime').strip()
            
            # Author (from landing page)
            author = landing_soup.find('div', {'class': 'article-author'}).get_text().split('by:')[1].strip()
            
            # Abstract (from landing page)
            tags = landing_soup.find_all(attrs={"data-block-key": True})
            if len(tags) >= 2:
                abstract = tags[1].get_text(strip=True)
            else:
                abstract = None
                        
            # Link (from landing page): DOI link, rather than `link_to_landing_page`,
            # is recorded as the `link` entry
            link = landing_soup.find('div', {'class': 'col-12 references citations'}).find('a')['href']
            
            # Number (from DOI link): Use the last few characters `link` to reliably procure the number
            number = link.split('RWP')[1].strip()

            data.append({
                'Title': title,
                'Date': date,
                'Author': author,
                'Abstract': abstract,
                'Link': link,
                'Number': number
            })

        return data

