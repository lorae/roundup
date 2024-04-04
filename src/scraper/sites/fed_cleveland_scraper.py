from ..generic_scraper import GenericScraper
from src.scraper.get_soup import selenium_soup

class FedClevelandScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'FED-CLEVELAND')

    def fetch_data(self):
        url = "https://www.clevelandfed.org/publications/working-paper"
        # Use Selenium to parse the webpage, return soup
        soup = selenium_soup(url=url)
        elements = soup.find_all('li', {'class': 'result-item'})

        # Initialize `data`
        data = []
        for el in elements:
            # Get the title
            title = el.find('h5').text.strip()
            print(title)
           
            # Get the link
            link = 'https://www.clevelandfed.org' + el.find('h5').find('a')['href']
            print(link)
            
            # Get the number
            # I'd use the link for this, since the links do contain the number, but sometimes the urls
            # have inconsistencies (e.g. writing '23-16' instead of '2316'. I've decided to use a different
            # element to get the number.
            date_number = el.find('div', {'class': 'date-reference'}).get_text().split("|")
            number = date_number[1].replace("WP", "").strip()
            print(number)
            
            # Get the date. Use above defined `date_number` to get the date
            date = date_number[0].strip()
            print(date)
            
            # Get the abstract
            abstract = el.find('div', {'class': 'page-description'}).get_text().strip()
            print(abstract)
            
            # Get the authors
            authors_list = el.find('div', {'class': 'authors'}).get_text().strip().split('\n')
            authors_string = ", ".join(authors_list)
            print(authors_string)

            # Populate `data` with new entries
            data.append({'Title': title,
                    'Link': link,
                    'Number': number,
                    'Date': date,
                    'Abstract': abstract,
                    'Author': authors_string})

        return data
