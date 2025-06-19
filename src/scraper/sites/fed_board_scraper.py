from ..generic_scraper import GenericScraper
from src.scraper.external_requests import request_soup
import requests

class FedBoardScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'FED-BOARD')
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
        number, and abstract for each working paper entry. 

        :return: A list of dictionaries containing Title, Author, Link, 
        Abstract, Number and Date for each working paper entry 
        :rtype: list
        '''
        url = 'https://www.federalreserve.gov/econres/feds/index.htm'
        # Bundle the arguments together for requests module
        session_arguments = requests.Request(method='GET', url=url, headers=self.headers)
        # Send request and get soup from landing page
        soup = request_soup(session_arguments)

        # Select all div elements with classes "col-xs-12", "col-md-9", and "heading" 
        # that do not have a "style" attribute. This effectively excludes the first 
        # element on the page which has the "style" attribute.
        elements = soup.select('div.col-xs-12.col-md-9.heading:not([style])')

        data = []
        for el in elements:
            title = el.select_one('h5 > a').text.strip()
            print(title)
            link = "https://www.federalreserve.gov" + el.select_one('h5 > a')['href']
            print(link)
            number = el.select_one('span.badge').text.strip().replace('FEDS ', '')
            print(number)
            authors = el.select_one('div.authors').text.strip()
            print(authors)
            abstract = el.select_one('div.collapse > p').text.strip().replace('Abstract: ', '')
            print("Here we go...")
            print(abstract)
            date = el.select_one('time')['datetime'] 
            print(date)
            print("yee haw")
            print(" ")
            print("......")

            data.append({
            'Title': title,
            'Link': link,
            'Number': number,
            'Author': authors,
            'Abstract': abstract,
            'Date': date
            })

        # Get titles, links, dates, and authors from the main website. Format them as a dictionary.
        # TODO: refactor this as one for loop to avoid redundant computation.
        # data = {
        #     'Title': title,
        #     'Link': link,
        #     'Number': number,
        #     'Author': authors,
        #     'Abstract': abstract,
        #     'Date': date
        # }

        return data