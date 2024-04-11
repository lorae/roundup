from ..generic_scraper import GenericScraper
from src.scraper.get_soup import request_soup
import requests
import re

class FedMinneapolisScraper(GenericScraper):
    # TODO: Check if this source has an API that can be scraped
    def __init__(self):
        super().__init__(source = 'FED-MINNEAPOLIS')
        # Define generic headers to be used later in the class
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

    def fetch_data(self):
        url = "https://www.minneapolisfed.org/economic-research/working-papers"
        # Bundle the arguments together for requests module
        session_arguments = requests.Request(method='GET', url=url, headers=self.headers)
        # Send request and get soup
        soup = request_soup(session_arguments)

        # Extract the elements containing data on working papers
        # Only use the most recent 10 elements: There are many, many going back to the 
        # 1970s, and parsing through them all is unnecessary. They appear to publish 
        # infrequently, so 10 entries seems ample.
        elements = soup.select('.i9-c-related-content__group--item')[:10]

        # Initialize `data`
        data = []
        for el in elements:
            title_element = el.select_one('.i9-c-related-content__group--title')
            number_element = el.select_one('.i9-c-related-content__group--date')
            
            # Extract title, number, and link from main landing page
            title = title_element.text.strip()
            number = number_element.text.split('Working Paper ')[1].split('(')[0].strip()
            link = 'https://www.minneapolisfed.org' + title_element['href']

            ### Access each individual WP landing page to get specific publication dates,
            ### abstracts, and authors
            # Bundle the arguments together for requests module
            session_arguments = requests.Request(method='GET', url=link, headers=self.headers)
            # Send request and get soup
            landing_soup = request_soup(session_arguments)

            # Extract the date. Note that the string is either split by the word "Published" or the word
            # "Revised" - which ever applies.
            date_text = landing_soup.select_one('.i9-c-title-banner__title--date').text
            # Use a regular expression to split the string on either "Published" or "Revised"
            # The pattern 'Published|Revised' tells the split function to match either "Published" or "Revised"
            split_date = re.split('Published|Revised', date_text)
            # Check if the split operation found a match and returned more than one element
            if len(split_date) > 1:
                date = split_date[1].strip()  # Take the part after "Published" or "Revised" and strip whitespace
            else:
                date = None  # or some default value, depending on how you want to handle cases without these keywords
            
            ## Extract the abstract
            abstract = landing_soup.find("p", class_="i9-e-p__large i9-js-markdown").text.strip()
            
            ## Extract the authors by selecting each element, and turning into a list.
            author_divs = landing_soup.find_all("div", class_="i9-c-person-block--small__content--name")
            authors = []
            for div in author_divs:
                author_name = div.find('a').text.strip() 
                authors.append(author_name)
            # Un-list the authors into a text string separated by commas
            author = ', '.join(authors)

            # Add each new data point to a data dictionary
            data.append({
                'Title': title,
                'Number': number,
                'Link': link,
                'Date': date,
                'Abstract': abstract,
                'Author': author
            })

        return data