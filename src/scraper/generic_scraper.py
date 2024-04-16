from abc import ABC, abstractmethod
import pandas as pd

class GenericScraper(ABC):
    def __init__(self, source):
        '''
        Initialize the GenericScraper with a source identifier.

        :param source: Identifier for the source of the data being scraped.
        :type source: str
        '''
        self.source = source

    @abstractmethod
    def fetch_data(self):
        '''
        Abstract method to be implemented by each subclass to fetch data specific to the scraper.

        This method should return a list of dictionaries, each representing an item to be scraped,
        with keys including 'Title', 'Link', 'Date', 'Abstract', 'Author', 'Number'.

        :return: A list of dictionaries containing scraped data.
        :rtype: list
        '''
        pass

    def fetch_and_process_data(self):
        '''
        Initiates the data fetching process by invoking the subclass-specific `fetch_data` method.
        Following data retrieval, this method processes the fetched data into a standardized pandas DataFrame,
        adding a 'Source' column to identify the data's origin and using a combination of 'Source' and 'Number'
        as a unique index.

        :return: A DataFrame containing the processed data, with 'Source' column and unique index.
        :rtype: pandas.DataFrame
        '''
        # Call the subclass-specific data fetching method
        data = self.fetch_data() 
        # Format the resulting dictionary `data` as a dataframe and name
        # `df`
        df = pd.DataFrame(data)
        # Append a source column using `Source` attribute of the subclass
        df['Source'] = self.source

        # Define the desired column order and reorder columns
        column_order = ['Title', 'Author', 'Link', 'Abstract', 'Number', 'Date', 'Source']
        df = df[column_order]

        # Create unique ID index for each working paper entry by 
        # combining `Source` and `Number` columns
        df.index = df['Source'] + df['Number'].astype(str)
        
        # Ensure that the index column remains unnamed
        df.index.name = None
        
        return df
    
    def read_scraper_status(self, filename="scraper_status.txt"):
        '''Reads the status of each scraper from a given file.'''
        try:
            with open(filename, 'r') as file:
                status_dict = {line.split(',')[0]: line.strip().split(',')[1] for line in file if line.strip()}
            return status_dict
        except FileNotFoundError:
            return {}

    def write_scraper_status(self, status_dict, filename="scraper_status.txt"):
        '''Writes the updated status of each scraper to a given file.'''
        with open(filename, 'w') as file:
            for scraper, status in status_dict.items():
                file.write(f"{scraper},{status}\n")

    def update_scraper_status(self, source, is_successful, filename='streamlit/scraper_status.txt'):
        '''
        Updates the status of a scraper based on its success or failure.
        
        :param source: The name of the scraper (source of the data).
        :param is_successful: Boolean flag indicating whether the scrape was successful.
        :param filename: Filename where the scraper statuses are stored.
        '''
        # Read the current statuses
        status_dict = self.read_scraper_status(filename)
        
        # Update the status based on the recent scrape result
        status_dict[source] = 'on' if is_successful else 'off'
        
        # Write the updated statuses back to the file
        self.write_scraper_status(status_dict, filename)
