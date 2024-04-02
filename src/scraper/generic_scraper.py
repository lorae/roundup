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
        data = self.fetch_data()  # Call the subclass-specific data fetching method
        df = pd.DataFrame(data)
        df['Source'] = self.source
        df.index = df['Source'] + df['Number'].astype(str)
        df.index.name = None
        return df