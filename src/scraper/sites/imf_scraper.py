from ..generic_scraper import GenericScraper
from src.scraper.get_soup import request_soup
import requests
import feedparser
import re

class IMFScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'IMF')
        # Define generic headers to be used later in the class
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

    # Public method which is called from outside the class.
    def fetch_data(self):
        '''
        Sends a GET request to the source's main page and parses the 
        response using BeautifulSoup to get title, link, and date
        for each working paper entry. 
        A secondary GET request is made to each working paper's 
        landing page and parsed using BeautifulSoup to extract working 
        paper abstracts, authors, and numbers.

        :return: A list of dictionaries containing Title, Author, Link, 
        Abstract, Number and Date for each working paper entry 
        :rtype: list
        '''
        # TODO: Refactor this section using IMF API.
        # Example URL:
        # https://www.imf.org/en/Publications/Search#sort=relevancy&numberOfResults=20&f:series=[WRKNGPPRS]&DateTo=12%2F31%2F2024&DateFrom=1%2F1%2F2024
        url = "https://www.imf.org/en/Publications/RSS?language=eng&series=IMF%20Working%20Papers"
        f = feedparser.parse(url)

        # Initialize `data`
        data = []
        for entry in f.entries:
            # Title
            title = entry.title

            # Link
            link = entry.link

            # Date
            date = entry.published[:-14]

            # Abstract, author, and number are found on the landing pages
            # for each individual working paper
            # Bundle the arguments together for requests module
            session_arguments = requests.Request(method='GET', 
                                                url=link, 
                                                headers=self.headers)
            # Send request and parse soup using BeautifulSoup
            landing_soup = request_soup(session_arguments)

            # Abstract. This section of code is brittle. It finds all
            # elements <p> with class 'pub-desc' as candidate abstracts
            # and chooses the fourth candidate (index number 3) and 
            # extracts text. When this script uses an API call in the
            # future, it will be much less brittle.
            potential_abstracts = landing_soup.find_all('p', {'class': 'pub-desc'})
            abstract = potential_abstracts[3].text.strip()

            # Author. This section of code is brittle. It finds all
            # elements <p> with class 'pub-desc' as candidate authors
            # and chooses the first candidate (index number 0) and 
            # extracts text. When this script uses an API call in the
            # future, it will be much less brittle.
            potential_authors = landing_soup.find_all('p', {'class': 'pub-desc'})
            raw_author_text = potential_authors[0].text.strip()
            # Use regex to replace any sequence of whitespace characters (space, 
            # newline, etc.) with a single space
            clean_author_text = re.sub(r'\s+', ' ', raw_author_text)

            # Date. This section of code is brittle. It finds all
            # elements <p> with class 'pub-desc' as candidate authors
            # and chooses the second candidate (index number 1) and 
            # extracts text. When this script uses an API call in the
            # future, it will be much less brittle.
            potential_numbers = landing_soup.find_all('p', {'class': 'pub-desc'})
            raw_number_text = potential_numbers[4].text.strip()
            # Removing 'Working Paper No. ' from beginning and replace '/'
            # with '-'
            clean_number_text = raw_number_text.replace('Working Paper No.', '').replace('/', '-').strip()

            # Append title, link, date, abstract, author, and number
            # to `data`
            data.append({
                'Title': title,
                'Link': link,
                'Date': date,
                'Abstract': abstract,
                'Author': clean_author_text,
                'Number': clean_number_text
            })

        return data