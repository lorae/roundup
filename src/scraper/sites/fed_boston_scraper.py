from ..generic_scraper import GenericScraper
from src.scraper.external_requests import request_json, request_soup
from datetime import datetime
import requests
import warnings

class FedBostonScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'FED-BOSTON')

    # Public method which is called from outside the class.
    def fetch_data(self):
        '''
        Sends a GET request to the source's API and parses the JSON-
        formatted response to get title, link, and author for each
        working paper entry. If the current month is January, also will
        send a GET request corresponding to the previous year's data.
        A secondary GET request is made to each working paper's 
        landing page and parsed using BeautifulSoup to extract
        date, number, and abstract data.

        :return: A list of dictionaries containing Title, Author, Link, 
        Abstract, Number and Date for each working paper entry 
        :rtype: list
        '''
        # TODO: Consider rewriting so that current and prior year are 
        # always scraped. May increase computing time but also increase 
        # simplicity for future development.
        # We may need to make two API calls, one for each year, if the month is close enough to the prior year (i.e.,
        # if the current month is January).
        url = 'https://www.bostonfed.org/api/pubsanddata/publications'
        # Get the current year and month
        current_year = datetime.now().year
        current_month = datetime.now().month
        if current_month == 1:
            print('current month is January')
            # Look at the current year's and last year's entries
            url_year_list = [current_year, current_year - 1]
        else:
            # Only look at the current year's entries
            url_year_list = [current_year]
        print(url_year_list)

        # Initialize `data`
        data = []
        # Loop through all of the url_year_list API calls. There will be one page to loop through - corresponding with
        # the current year - if the current month is NOT January. If the current month IS Janury, both this year's
        # and last year's main pages will be scraped.
        for year in url_year_list:
            # These headers (and params) are highly specific to the API call, so unlike some other subclasses of GenericScraper, 
            # in this class, the headers are defined within fetch_data.
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-GPC': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Cookie': ''
            }
            payload = {'yr': f'{year}', # API call payload depends on year
                'jel': '',
                'type': '',
                'series': '8c2cb55e251349c59d19db1040c20368',
                'vol': '',
                'siteTpc': '',
                'dept': '',
                'author': '',
                'focus': '',
                'program': '',
                'services': '',
                'center': '',
                'yrFrom': '',
                'yrTo': '',
                'd': 'false',
                'dt': 'false',
                'srt': '0',
                'pgSz': '20',
                'pgN': '1'
                }
            # Send API request and parse JSON response
            response = request_json(method = 'GET', 
                                    url = url, 
                                    headers = headers, 
                                    params = payload)
            entries = response['publications']

            for entry in entries:
                # Title
                title = entry['title']

                # Author names are stored within itemAuthors attribute. Loop through itemAuthors
                # and join each author fullName with ", " to generate one `authors` string.
                authors = ", ".join([author['fullName'] for author in entry['itemAuthors']])

                # Link
                link = 'https://www.bostonfed.org/' + entry['url']

                # Now we visit the individual entry page to extract abstract, number, and date.
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"}
                # Bundle the arguments together for requests module
                session_arguments = requests.Request(method='GET', url=link, headers=headers)
                # Send request and get soup from landing page
                soup = request_soup(session_arguments)

                # Getting the abstract from the individual WP page
                abstract = soup.find('div', {'id': 'collapse3'}).get_text().strip()

                # Getting the number from the individual WP page
                number = soup.find('p', {'class': 'doi-text'}).get_text().split("No. ")[1].split("https:")[0].replace(".", "").strip()

                # Getting the publication date from the individual WP page
                meta_tag = soup.find('meta', {'property': 'article:published_time'})
                if meta_tag and meta_tag.has_attr('content'):
                    # Extract the content attribute and then split it to get the date part
                    date = meta_tag['content'].split('T')[0]
                else:
                    date = None
                    warnings.warn("Meta tag not found or doesn't have a 'content' attribute.")

                # Append title, author, link, abstract, number, date to the
                # `data` dictionary list
                data.append({
                    'Title': title,
                    'Author': authors,
                    'Link': link,
                    'Abstract': abstract,
                    'Number': number,
                    'Date': date
                })

        return data


