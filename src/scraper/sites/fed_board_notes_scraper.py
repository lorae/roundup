from src.scraper.get_soup import request_soup
from ..generic_scraper import GenericScraper
from datetime import datetime
import requests

class FedBoardNotesScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'FED-BOARD-NOTES')
        # Define headers once and use them throughout the class
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

    def fetch_data(self):
        url_list = ['https://www.federalreserve.gov/econres/notes/feds-notes/default.htm']
        # Get the current year and month
        current_year = datetime.now().year
        current_month = datetime.now().month

        # If the current month is January, also look at last year's entries.
        if current_month == 1:
            print('current month is January')
            # Create a URL for the current year
            last_year_url = f'https://www.federalreserve.gov/econres/notes/feds-notes/{current_year-1}-index.htm'
            print(last_year_url)
            url_list += [last_year_url]

        print(url_list)

        # Initialize `data`
        data = []
        # Loop through all of the Fed Notes URL pages. There will be one page to loop through - corresponding with
        # the current year - if the current month is NOT January. If the current month IS Janury, both this year's
        # and last year's main pages will be scraped.
        for url in url_list:
            # Bundle the arguments together for requests module
            session_arguments = requests.Request(method='GET', url=url, headers=self.headers)
            # Send request and get soup from landing page
            soup = request_soup(session_arguments)
            elements = soup.select('div.col-xs-12.col-md-9.heading.feds-note:not([style])')

            # Loop through relevant elements on main page
            for el in elements:
                title = el.find('h5').text.strip()               
                author = el.find('div', class_='authors').text.strip()          
                date = el.find('time')['datetime']
                abstract = el.find_all('p')[1].text.strip()
                # DOI links were originally used in this script, but DOI URLs on this page broke in February 2024. 
                # After I notified the Fed Board of this issue, they fixed it. But just in case, I have migrated to using 
                # the href URL that accompanies the title of the paper, rather than the DOI.
                # second p element, slice off the first 4 chars (that say "DOI:")
                doi_link = el.find_all('p')[2].text[4:].strip() # doi link
                href_link = 'https://www.federalreserve.gov/' + el.find('h5').find('a')['href'] # href link           
                # This website doesn't number papers, so I designate numbers to be the end part of the DOI url
                number = doi_link.split('.org')[1].replace('.', '').replace('/', '').replace('-', '').strip()        
                
                # Populate `data` with new entries
                data.append({'Title': title,
                             'Author': author,
                             'Date': date,
                             'Abstract': abstract,
                             'Link': href_link, # replacing with doi_link here is also fine
                             'Number': number})
        
        return data