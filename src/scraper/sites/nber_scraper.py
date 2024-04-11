from ..generic_scraper import GenericScraper
from src.scraper.get_soup import request_json, request_soup
import requests
import re

class NBERScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'NBER')
        # Define generic headers to be used later in the class
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

    def fetch_data(self):
        url = 'https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=100'
        # Send request and parse JSON-formatted response
        response = request_json(method = 'GET',
                            url = url,
                            headers = self.headers)
        elements = response['results']

        # Initialize `data`
        data = []

        for el in elements:
            # Title
            title = el['title']

            # Link
            link = 'https://www.nber.org' + el['url']

            # Date
            date = el['displaydate']

            # Number
            number = el['url'].split('/papers/w')[1]

            # Visit each working paper's landing page to gather abstract
            # and author
            # Bundle the arguments together for requests module
            session_arguments = requests.Request(method='GET', 
                                                url=link, 
                                                headers=self.headers)
            # Send request and parse soup using BeautifulSoup
            landing_soup = request_soup(session_arguments)

            # Abstract
            abstract = landing_soup.find('div', {'class': 'page-header__intro-inner'}).text.strip()

            # Author
            raw_author_text = landing_soup.find('div', {'class': 'page-header__authors js-expandable-list'}).text.strip()
            # Use regex to replace any sequence of whitespace characters (space, 
            # newline, etc.) with a single space
            clean_author_text = re.sub(r'\s+', ' ', raw_author_text)

            # Append title, link, date, number, abstract, clean_author_text
            # to `data`
            data.append({
                'Title': title,
                'Link': link,
                'Date': date,
                'Number': number,
                'Abstract': abstract,
                'Author': clean_author_text
            })
        
        return(data)


