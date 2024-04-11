from ..generic_scraper import GenericScraper
from src.scraper.get_soup import request_soup
import requests
from bs4 import BeautifulSoup
import re
import PyPDF2
import io

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
        url = "https://www.dallasfed.org/research/papers"
        # Bundle the arguments together for requests module
        session_arguments = requests.Request(method='GET', url=url, headers=self.headers)
        # Send request and get soup
        soup = request_soup(session_arguments)

        # Find all the h3 tags. These act as signposts that definitively separate working
        # paper entries. We limit ourselves to only the first 20 h3 tags since they entries
        # go all the way back to the 1980s.
        h3_tags = soup.find_all('h3')[:20]
        count = 0

        # Initialize `data`
        data = []
        for h3 in h3_tags:
            
            # Get the number from the h3 tag.
            number = h3.text
            # Check if 'Globalization Institute' is in the number string. Replace with "GI"
            if 'Globalization Institute' in number:
                number = number.replace('Globalization Institute No. ', 'GI')

            # Get the title from the first p tag that follows the h3 tag.
            next_p = h3.find_next_sibling('p')
            title = next_p.find('strong').text if next_p.find('strong') else None

            # Get the link from the first p tag that follows the h3 tag. Note that this is a link to a pdf, NOT 
            # a landing page. Some working papers have landing pages, but it is inconsistent.
            link = "https://www.dallasfed.org" + next_p.find('a')['href']

            # The author also comes from the first p tag that follows the h3 tag. But it is 
            # complicated to extract since it doesn't have its own element. The cleanest way to extract
            # the data is to parse the element as text and then convert back to a beautiful soup to then
            # once again extract the clean text.
            # 1. Convert the p tag's contents to a string and find the location where "Abstract:" appears.
            abstract_location = str(next_p).find('Abstract:')
            # 2. Extract the substring that precedes "Abstract:".
            html_before_abstract = str(next_p)[:abstract_location]
            # 3. Parse the extracted substring using BeautifulSoup.
            soup_fragment = BeautifulSoup(html_before_abstract, 'html.parser')
            # 4. Find the last a tag within this fragment.
            last_a_tag = soup_fragment.find_all('a')[-1]
            # 5. In the original p tag, find the <br> tag right after the last a tag.
            br_tag_after_last_a = last_a_tag.find_next('br')
            # 6. Find the <strong> tag right after the <br> tag.
            author_tag = br_tag_after_last_a.find_next('strong')
            # 7. Extract the text.
            author = author_tag.text

            # Get the abstract. Methodology similar to author above.
            # There's room for improvement in this code, and perhaps a better solution is using the PDF,
            # as is done for the paper date.
            # 1. Find the position where "Abstract:" appears in next_p's contents.
            abstract_start = str(next_p).find('Abstract:') + len('Abstract:')
            # 2. Get the substring starting from "Abstract:".
            substring_after_abstract = str(next_p)[abstract_start:]
            # 3. Find the position of the first line break (either <br>, <br/>, or </br>) after "Abstract:" in the substring.
            match = re.search(r'<br ?/?>|</br>', substring_after_abstract)
            if match:
                abstract_end = match.start()
            else:
                abstract_end = len(substring_after_abstract)  # if no match found, use the full length
            # 4. Extract the desired abstract text by converting back to a soup, and then again to text. This removes unneeded 
            # <p> and <br> tags and the like.
            abstract_html = substring_after_abstract[:abstract_end].strip()
            abstract_soup = BeautifulSoup(abstract_html, 'html.parser')
            abstract = abstract_soup.get_text()

            # Get the date from PDF file. Complicated.
            # Link = ["https://www.dallasfed.org/-/media/documents/research/papers/2023/wp2305.pdf"]
            # The extract_date function doesn't always work because sometimes the text has spaces and line breaks
            # that mess up the regex (e.g. "M ay 5, 2023" instead of "May 5, 2023"). I'd like to also extract the abstract
            # from the PDF but I need to learn how to remove the unnecessary line breaks and spaces first. The above link
            # is an example of a PDF that produces this error. Most work, however.
            # Get the PDF content for the current row
            pdf_content = requests.get(link).content
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        
            # Extract the text from the second page
            text = pdf_reader.pages[1].extract_text().replace('\n', ' ')
            date = self.extract_date(text)

            data.append({
                'Number': number,
                'Title': title,
                'Link': link,
                'Author': author,
                'Abstract': abstract,
                'Date': date
            })

        return data

    # Private method used to extract date from parsed pdf content   
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