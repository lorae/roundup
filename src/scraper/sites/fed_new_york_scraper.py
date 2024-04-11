from ..generic_scraper import GenericScraper
from src.scraper.get_soup import request_json, request_soup
from datetime import datetime
import requests
import warnings

class FedNewYorkScraper(GenericScraper):
    # TODO: Check if this source has an API that can be scraped
    def __init__(self):
        super().__init__(source = 'FED-NEWYORK')
        # Define generic headers to be used later in the class
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

    # Public method which is called from outside the class.
    def fetch_data(self):
        '''
        Sends a GET request to the source's main page and parses the 
        response using BeautifulSoup. Method also will send a similar 
        GET request corresponding to the previous year's entries. From 
        these main landing pages, extracts title, link, 
        author, date, and number for each working paper entry. 
        A secondary GET request is made to each working paper's 
        landing page and parsed using BeautifulSoup to extract working
        paper abstracts.

        :return: A list of dictionaries containing Title, Author, Link, 
        Abstract, Number and Date for each working paper entry 
        :rtype: list
        '''
        # Define the current and last year
        current_year = datetime.now().year
        last_year = current_year - 1

        # Initialize `data`
        data = []
        # Prepare two urls for API requests: one with the current year, and one with the 
        # last year. This type of request is useful in the edge case when the current date
        # is in early January and recently published papers could have been published last 
        # year.
        url_list = [f'https://www.newyorkfed.org//api/research/getsritemshtml?year={current_year}&useLucene=true',
                    f'https://www.newyorkfed.org//api/research/getsritemshtml?year={last_year}&useLucene=true']
        for url in url_list:
            print(f"Scraping {url}")
            # Use custom request_json function to make GET request and parse JSON response
            response = request_json(method = 'GET',
                                    url = url,
                                    headers = self.headers)

            for entry in response:
                # Title
                title = entry.get("Paper_Title").strip() or None 

                # Author
                author = entry.get("AuthorsHtml").strip() or None
                
                # Date
                date = entry.get("PublicationDate") or None
                
                # Link: Ensure 'Uri' is present in the entry before proceeding.
                if 'Uri' in entry and entry.get('Uri'):
                    link = 'https://www.newyorkfed.org/' + entry.get('Uri')
                else:
                    # If link is not present, skip this iteration of loop and produce warning.
                    warnings.warn(
                        f'No link listed for the entry with title {title}. '
                        f'Data not logged. Skipping to next working paper.'
                    )
                    continue

                # Number: Essential component, so fallback is last four elements of
                # `link`
                # Attempt to assign 'Series_Number' or fallback to None
                number = entry.get("Series_Number", "").strip() or None
                if number == None:
                    # If no number found, extract the last 4 characters of `link`
                    # and use as the number
                    number = link[-4:].strip()

                # Abstract: Request each landing page and parse as Beautiful Soup
                # Bundle the arguments together for requests module
                session_arguments = requests.Request(method='GET', url=link, headers=self.headers)
                # Send request and get landing_soup
                landing_soup = request_soup(session_arguments)
                abstract = landing_soup.select('div.ts-article-text')[1].text.strip().replace('\n', ' ')

                # Append title, author, date, link, number, and abstract to the
                # `data` dictionary list
                data.append({
                    'Title': title,
                    'Author': author,
                    'Date': date,
                    'Link': link,
                    'Number': number,
                    'Abstract': abstract
                })

        return data



   
