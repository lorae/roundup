from src.scraper.external_requests import selenium_soup
from ..generic_scraper import GenericScraper

class ECBScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'ECB')
    
    # Public method which is called from outside the class.
    def fetch_data(self):
        # TODO: Store data in list of dictionaries like most of the 
        # other fetch_data() methods.
        '''
        Uses Selenium to access the source's main page and parses the 
        output using BeautifulSoup to get title, link, author, date, 
        number, and abstract for each working paper entry. 

        :return: A list of dictionaries containing Title, Author, Link, 
        Abstract, Number and Date for each working paper entry 
        :rtype: list
        '''
        url = 'https://www.ecb.europa.eu/pub/research/working-papers/html/index.en.html'
        # Send request and get soup
        soup = selenium_soup(url)
        # Extract elements from soup
        elements = soup.find('dl', {'class': 'ecb-basicList wpSeries ecb-lazyload pub-list-filter'})

        # Filter to keep only the <dt> tags that have the 'isodate' attribute (if they do not
        # have this attribute, then they do not correspond with data on a specific working paper).
        filtered_dt_elements = [dt for dt in elements.find_all('dt') if dt.has_attr('isodate')]

        # Initialize lists to store data
        Date = []
        Title = []
        Author = []
        Abstract = []
        Link = []
        Number = []

        # Loop through the filtered <dt> and corresponding <dd> tags.  <dt> tags contain the date.
        # All other information is in the <dd> tags.
        for dt in filtered_dt_elements[:20]: # only selecting first 20 elements - we don't need them all
            dd = dt.find_next_sibling('dd')  
            if not dd:
                # Skip to the next iteration of the for loop. Do not log data for this entry.
                continue

            # Date (from dt tag)
            date_div = dt.find('div', class_='date')
            date = date_div.text if date_div else "No date"
            Date.append(date)

            # Title
            title_div = dd.find('div', class_='title')
            title = title_div.text if title_div else "No title"
            Title.append(title)

            # Author
            author_list = dd.find_all('li')
            author = ', '.join([li.text for li in author_list]) if author_list else "No authors"
            Author.append(author)

            # Abstract
            abstract_dd = dd.find('dd')
            abstract = abstract_dd.text if abstract_dd else "No abstract"
            Abstract.append(abstract)

            # Link
            if title_div:
                link_a = title_div.find('a')
                link = "https://www.ecb.europa.eu"+ link_a['href'] if link_a else "No link"
            else:
                link = "No link"
            Link.append(link)

            # Number
            number_div = dd.find('div', {'class': 'category'})
            number = number_div.text.replace("No. ", "") if number_div else "No number"
            Number.append(number)

        # Create a dictionary of the six lists, where the keys are the column names.
        data = {'Title': Title,
                'Link': Link,
                'Date': Date,
                'Author': Author,
                'Number': Number,
                'Abstract': Abstract}
        
        # Use the inherited process_data method to create and return the DataFrame
        return data