from ..generic_scraper import GenericScraper
from src.scraper.get_soup import request_soup
import requests
import json
from html import unescape

class FedPhiladelphiaScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'FED-PHILADEPHIA')
        # Define generic headers to be used later in the class
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

    def fetch_data(self):
        url = 'https://www.philadelphiafed.org/search-results/all-work?searchtype=working-papers'
        # Bundle the arguments together for requests module
        session_arguments = requests.Request(method='GET', 
                                             url=url, 
                                             headers=self.headers)
        # Send request and get parse soup using BeautifulSoup
        soup = request_soup(session_arguments)
        
        # There are many <script> tags in this website's HTML, and the 
        # order in which they appear often varies. Rather than searching 
        # for the n-th <script> tag, this script instead locates the keyword 
        # "Working Paper", which is unique to the script tag that contains 
        # the json-formatted data set with all the working paper contents
        for script in soup.find_all('script'):
            if "Working Paper" in script.get_text():
                json_element = script
                break

        # Tweak the formatting of json_element so it is valid JSON data.
        # First, remove text before the key "data:". Then, remove the } }) 
        # at the end of json_element.
        json_str = json_element.string.split('data: ')[1].split('})')[0].strip()[:-1]
        # Parse the JSON string into a Python dictionary
        json_data = json.loads(json_str)

        # Initialize `data`
        data = []
        # Loop through individual working paper entries in json_data
        for wp in json_data['results']:
            # Extract title. Note: unescape ensures that characters 
            # like the apostrophe don't appear as &ldquo;, &rdquo;, and 
            # &rsquo
            title = unescape(wp['attributes']['title'])

            # Extract author_string. Authors are first counted as a list
            # and then individual names are joined with the ', ' separator
            # to make an author_string
            author_list = wp['attributes']['authors']
            # Create the author string from the author list
            author_string = ', '.join([author['name'] for author in author_list])

            # Number: There are <em></em> tags all over the place that
            # need to be removed. After those are gone, remove the 'WP ' part
            # of the string and keep only the first 5 characters of what 
            # remains, which represent the number.
            number = wp['attributes']['excerpt'].replace('<em></em>', '').split('WP ')[1][:5] 

            # Link
            link = 'https://www.philadelphiafed.org' + wp['attributes']['url']

            # Visit the individual wp landing page to obtain data on
            # abstract and date
            # Bundle the arguments together for requests module
            session_arguments = requests.Request(method='GET', 
                                                url=link, 
                                                headers=self.headers)
            # Send request and get parse soup using BeautifulSoup
            landing_soup = request_soup(session_arguments)

            # Abstract: first find relevant <div> tag with class 'article-body'
            abstract_element = landing_soup.find('div', {'class': 'article-body'})
            # Extract text from all <p> tags within the abstract_element
            p_tags = abstract_element.find_all('p')
            # Join the contents of the <p> tags with a space, remove white space
            # and remove newline '\n' characters
            abstract = ' '.join(p.text for p in p_tags).strip().replace('\n', '')

            # Extract the publication date from landing page
            # Formerly the PDF moddate was used for a more precise date,
            # but the code was overly complex, and this does the job.
            date = landing_soup.find('p', {'class': 'article-date-published'}).text.strip()

            # Append title, author_string, number, link, abstract, and date
            # to `data`

            data.append({
                'Title': title,
                'Author': author_string,
                'Number': number,
                'Link': link,
                'Abstract': abstract,
                'Date': date
            })

        return data


