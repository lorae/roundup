from ..generic_scraper import GenericScraper
from src.scraper.get_soup import request_soup
import requests

class FedChicagoScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = "FED-CHICAGO")
        # Define headers once and use them throughout the class
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }
    

    # Public method which is called from outside the class.
    def fetch_data(self):
        url = "https://www.chicagofed.org/publications/publication-listing?filter_series=18"
        # Bundle the arguments together for requests module
        session_arguments = requests.Request(method='GET', url=url, headers=self.headers)
        # Send request and get soup
        soup = request_soup(session_arguments)
        elements = soup.find_all('div', {'class': 'cfedPublicationListing'})

        # First pass where we get the list of elements from the URL and extract relevant information
        data = []
        for element in elements:
            # The name of the tag we use to get the title and link
            title_link_tag = element.find('a', {'class': 'cfedPublicationListing--title'})
            # Get the title
            title = title_link_tag.text.strip()
            # Get the link
            link = "https://www.chicagofed.org" + title_link_tag['href']
            # Get the number
            number = link.split("/")[-1]

            # Here, we're assuming that the year and month are always at index 1 and 4, respectively, in the info_text list.
            # Also, we're assuming that these strings can be safely stripped of whitespace and turned into integers.
            info_text = element.find('div', {'class': 'cfedPublicationListing--info'}).text.strip().split("|")
            # Get the author
            author = info_text[0].strip()
            # Get the date
            year = str(info_text[1].strip())
            month = info_text[4].strip()
            date = month + " " + year

            # Get the abstract. This requires visiting the landing page,
            # given by link, for each WP.
            # Bundle the arguments together for requests module
            session_arguments = requests.Request(method='GET', url=link, headers=self.headers)
            # Send request and get soup
            landing_soup = request_soup(session_arguments)
            abstract_tags = landing_soup.find('div', {'class': 'cfedArticle__introParagraph'})
            if abstract_tags:
                abstract = abstract_tags.text.strip()  # return the text
            else:
                abstract = None  # return None if the tag is not found

            # Append title, link, number, author, date, abstract to the `data` dictionary
            data.append({
                'Title': title,
                'Link': link,
                'Number': number,
                'Author': author,
                'Date': date,
                'Abstract': abstract
            })

        return data
