from src.scraper.get_soup import request_soup
from ..generic_scraper import GenericScraper
import requests
from bs4 import BeautifulSoup

class BFIScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'BFI')
        # Define headers once and use them throughout the class
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }
    
    # Public method which is called from outside the class.
    def fetch_data(self):
        url = 'https://bfi.uchicago.edu/working-papers/'
        # Bundle the arguments together for requests module
        session_arguments = requests.Request(method='GET', url=url, headers=self.headers)
        # Send request and get soup
        soup = request_soup(session_arguments)

        elements = soup.select('div.teaser.teaser--working-paper ')

        # Get titles, links, dates, and authors from the main website
        Titles = [el.select('h2.teaser__title')[0].text.strip() for el in elements]
        Links = [el.select('h2.teaser__title a')[0]['href'] for el in elements]
        Dates = [el.select('span.meta__date')[0].text.strip() for el in elements]
        Authors = [el.select('div.teaser__names')[0].text.strip() for el in elements]

        # Get the abstracts and numbers (href attributes)
        Abstracts = []
        Numbers = []

        for link in Links:
            # Bundle the arguments together for requests module
            session_arguments = requests.Request(method='GET', url=link, headers=self.headers)
            # Send request and get soup
            soup = request_soup(session_arguments)
            
            # Get the abstracts
            abstract = soup.select('div.textblock')[0].text.strip()
            Abstracts.append(abstract)
            
            # Get the href attribute of 'a.button'
            number = soup.select('a.button')[0]['href'].split('BFI_WP_')[1].replace('.pdf', '')
            Numbers.append(number)
            
        # Create a dictionary of the six lists, where the keys are the column names.
        data = {'Title': Titles,
                'Link': Links,
                'Date': Dates,
                'Author': Authors,
                'Number': Numbers,
                'Abstract': Abstracts}
        
        # Use the inherited process_data method to create and return the DataFrame
        return data
