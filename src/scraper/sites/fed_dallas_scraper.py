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
            # Find the table containing working paper metadata
            table = soup.find('div', {'class': 'dal-tab__pane', 'id': year_id})
            
            if table:
                # Within the table, extract the <p> elements
                elements = table.find_all('p')
                for e in elements:
                    # Not all the p elements contain useful information. Screen them using
                    # is_relevant_p_tag
                    if self.is_relevant_p_tag(e):
                        title_tag = e.find('a', href=True)
                        title = title_tag.text.strip() if title_tag else "Title not found"

                        # The title tag also contains an href link pointing to the paper PDF
                        link = "https://www.dallasfed.org" + title_tag['href']

                        number = self.extract_paper_number(e)
                        
                        # Get the entire text content of the paragraph
                        e_text = e.get_text(separator="\n")
                        # The authors appear after the title and before the text
                        # "Abstract"
                        author_text = e_text.split(title)[1].split("Abstract:")[0]
                        # Remove the word "Codes" if it appears in the string
                        author = author_text.replace("Codes", "").strip()

                        # Use the entire paragraph text to get the abstract
                        abstract = e_text.split("Abstract:")[1].strip()

                        # Get the date from PDF file. Complicated.
                        pdf_content = requests.get(link).content
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
                            'Author': author,
                            'Abstract': abstract,
                            'Date': date
                        })

        return data

    # Check whether a given element contains working paper data like 
    # title, abstract, and author.
    def is_relevant_p_tag(self, element):
        # Find all <a> tags with an href attribute within the given element
        a_tags = element.find_all('a', href=True)
        
        # Check if any <a> tags contain links to a PDF
        for a in a_tags:
            if a['href'].endswith('.pdf'):
                return True

        # If no PDF link is found, the element is not relevantS
        return False

    def extract_paper_number(self, element):
        """
        Extracts the paper number from a <strong> element within the given element.
        The paper number starts with either "Globalization Institute No." or "No."
        and is followed by a number.
        
        :param element: BeautifulSoup object representing a tag containing a <strong> tag with the paper number.
        :return: The extracted paper number or "Number not found" if the pattern is not matched.
        """
        # Find the <strong> tag that contains the number
        strong_tag = element.find('strong')
        
        if not strong_tag:
            return "Number not found"

        # Get the text content from the <strong> tag
        strong_text = strong_tag.text.strip()

        # Define the pattern to match "Globalization Institute No." or "No." followed by the number
        pattern = r"^(Globalization Institute No\. \d+|No\. \d+)"

        # Search for the pattern in the text
        match = re.match(pattern, strong_text)

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