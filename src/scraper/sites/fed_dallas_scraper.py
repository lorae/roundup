from ..generic_scraper import GenericScraper
from src.scraper.external_requests import request_soup
import requests
import re
import PyPDF2
import io
from datetime import datetime

class FedDallasScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'FED-DALLAS')
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
        and number for each working paper entry. 
        A secondary GET request is used to access the working paper 
        itself, with content parsed using made to each working paper's 
        landing page and parsed using PyPDF2 and io to extract working
        paper abstracts.

        :return: A list of dictionaries containing Title, Author, Link, 
        Abstract, Number and Date for each working paper entry 
        :rtype: list
        '''
        url = "https://www.dallasfed.org/research/papers"
        # Bundle the arguments together for requests module
        session_arguments = requests.Request(method='GET', url=url, headers=self.headers)
        # Send request and get soup
        soup = request_soup(session_arguments)

        # Initialize `data`
        data = []

        # Get the current year and the previous year
        current_year = datetime.now().year
        previous_year = current_year - 1

        # Extract data for the current and previous year
        for year_id in [str(current_year), str(previous_year)]:
            # Find the container containing working paper metadata
            container = soup.find('div', {'class': 'dal-tab__pane', 'id': year_id})
            table = container.find('div', {'class': 'dal-citations__inline--wp-index'})
            elements = table.find_all('div', class_='dal-index-item')
            #print(elements)

            for el in elements:
                # Number
                number_text = el.select_one('p.dal-tagline').text.strip()
                number = self.extract_paper_number(number_text)

                # Title and link
                title_tag = el.select_one('p.dal-headline > a')
                title = title_tag.text.strip()
                link = "https://www.dallasfed.org" + title_tag['href']

                # Authors
                authors = el.select_one('p.dal-author').text.strip()

                # Abstract
                abstract_tag = el.select_one('div.dal-abstract > p')
                abstract = abstract_tag.text.strip().replace("Abstract: ", "") if abstract_tag else ""

                # PDF link
                pdf_link_tag = el.select_one('div.dal-abstract a[href$=".pdf"]')
                pdf_link = "https://www.dallasfed.org" + pdf_link_tag['href'] if pdf_link_tag else ""

                # Get the date from PDF file. Complicated.
                pdf_content = requests.get(pdf_link).content
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            
                # Extract the text from the second page
                text = pdf_reader.pages[1].extract_text().replace('\n', ' ')
                date = self.extract_date(text)

                # Append number, title, link, author, abstract, and date to the
                # `data` dictionary list
                data.append({
                    'Number': number,
                    'Title': title,
                    'Link': link,
                    'Author': authors,
                    'Abstract': abstract,
                    'Date': date
                })

        return data

    def extract_paper_number(self, text):
        """
        Extracts the paper number from a <strong> element within the given element.
        The paper number starts with either "Globalization Institute No." or "No."
        and is followed by a number.
        
        :param element: BeautifulSoup object representing a tag containing a <strong> tag with the paper number.
        :return: The extracted paper number or "Number not found" if the pattern is not matched.
        """
        # Define the pattern to match "Globalization Institute No." or "No." followed by the number
        pattern = r"^(Globalization Institute No\. \d+|No\. \d+)"

        # Search for the pattern in the text
        match = re.match(pattern, text)

        if match:
            # If found, return the matched text (the paper number)
            number = match.group()
            if 'Globalization Institute' in number:
                number = number.replace('Globalization Institute No. ', 'GI')
            if 'No.' in number:
                number = number.replace('No.', '').strip()

        else:
            number = "Number not found"

        return(number)
    
    # Extract date from parsed pdf content   
    def extract_date(self, text):
        # Remove line breaks
        cleaned_text = text.replace('\n', ' ')

        # Regex pattern to find the date
        date_pattern = re.compile(r'(?P<month>January|February|March|April|May|June|July|August|September|October|November|December)( \d{1,2},)? \d{4}')
        match = date_pattern.search(cleaned_text)

        if match:
            date = match.group()
        else:
            date = None

        return date