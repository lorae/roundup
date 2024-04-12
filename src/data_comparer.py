import pandas as pd
import os
import ast
from datetime import datetime


class HistoricDataComparer:
    '''
    A class to compare newly scraped data against a historical record set to identify novel entries.

    Attributes:
        historic_ids (set): Set of unique identifiers from previously observed data.

        current_datetime (str): Current date and time, formatted for file naming.

        current_date (str): Current date, formatted for data tagging.
    
    Constants:
        HISTORIC_IDS_FILEPATH (str): Filepath to the historic working paper identifiers. 
            This is where the historic registry of paper IDs is stored.
    '''
    # Class level constant signifying the file path to the historic working paper
    # identifiers data. This is the filepath where the historic registry of paper 
    # ids is stored
    HISTORIC_IDS_FILEPATH = 'data/historic_wp_ids.txt'

    def __init__(self):
        '''
        Initializes the HistoricDataComparer. Loads the historic set of identifiers 
        from the file specified by HISTORIC_IDS_FILEPATH.
        '''
        # This attribute loads the contents of the historic working paper ids file,
        # which are stored as a Python sets
        self.historic_ids = self.load_historic_ids()
        # Defining current dates and times for use in save_results() and
        # compare() methods
        self.current_datetime = datetime.now().strftime('%Y-%m-%d-%H%M')
        self.current_date = datetime.now().strftime('%m/%d/%Y')

    def load_historic_ids(self):
        '''
        Loads the set of historical identifiers from the file specified by HISTORIC_IDS_FILEPATH.

        Returns:
            set: A set of strings representing historic identifiers.

        Raises:
            FileNotFoundError: If the file specified by HISTORIC_IDS_FILEPATH does not exist.
        '''
        try:
            with open(self.HISTORIC_IDS_FILEPATH, 'r') as file:
                return ast.literal_eval(file.read())
        except FileNotFoundError:
            raise FileNotFoundError(f'File {self.HISTORIC_IDS_FILEPATH} not found.')

    def compare(self, df):
        '''
        Identifies novel entries by comparing the dataframe indices against the historic set.

        Parameters:
            df (pd.DataFrame): The dataframe with new data to compare.

        Returns:
            pd.DataFrame: A dataframe containing only the novel entries.
        '''
        # Define set of ids from recently scraped data
        recent_ids = set(df.index)
        # Determine set of novel entry ds by subtracting the historic 
        # set from the recent set
        novel_ids = recent_ids - self.historic_ids

        # Check if there are any novel entries
        if novel_ids:
            # Filter the recently scraped data for only the novel entries
            novel_df = df.loc[list(novel_ids)]
            # Add an estimated publication date column to novel entries
            novel_df['est_PubDate'] = self.current_date

            return novel_df
        else:
        # Return an empty DataFrame if there are no novel entries to ensure the method always returns a DataFrame
            return pd.DataFrame()

    def save_results(self, novel_df, base_path = 'data/local_scrape_outcomes'):
        '''
        Saves the novel entries in .csv, .txt, and .html formats into the specified base_path.

        Note:
            Output files are saved in a directory specified by `base_path`, which 
            is typically configured to be ignored by version control (.gitignore). 
            This setup is intended for local debugging and temporary storage. 
            See README for more details.

        Parameters:
            novel_df (pd.DataFrame): Data frame containing the novel entries, which are
            produced by applying the compare() method in this class to a data frame of recently
            scraped data.

            base_path (string): File path specifying the target directory for this method's
            output files.

        Outputs:
            .csv: Contains all novel entries with metadata. File is saved in `base_path`
            directory with name `YYYY-MM-DD-HHMM-data.csv`.

            .html: Browser-viewable dashboard file with clickable links for each entry 
            title. File is saved in `base_path` directory with name 
            `YYYY-MM-DD-HHMM-dashboard.html`.

            .txt: Contains the set of unique identifiers of the novel entries, formatted 
            as a Python set for potential future debugging. File is saved in `base_path` 
            directory with name `YYYY-MM-DD-HHMM-ids.txt`.
        '''

        # Create a template filepath, which will be used to save the below
        # .csv, .html, and .txt files
        filepath = os.path.join(base_path, self.current_datetime)

        # Save .csv
        # Write novel_df to file. Use utf-8 encoding to ensure special
        # characters are properly displayed.
        novel_df.to_csv(f'{filepath}-data.csv', encoding='utf-8')

        # Save .html
        # Copy novel_df and assign to df_html
        df_html = novel_df.copy()
        # Reset the index and drop the old index
        df_html = df_html.reset_index(drop=True)  
        # Add hyperlinks to the titles
        df_html['Title'] = df_html.apply(lambda row: f'<a href="{row["Link"]}">{row["Title"]}</a>', axis=1)
        # Drop the 'Link' and 'Number' columns
        df_html = df_html.drop(['Link', 'Number'], axis=1)
        html_content = df_html.to_html(escape=False)
        # Write html_content to file. Use utf-8 encoding to ensure special
        # characters are properly displayed.
        with open(f'{filepath}-dashboard.html', 'w', encoding='utf-8') as file:
            file.write(html_content)

        # Save .txt
        # Define novel_ids using indices from novel_df
        novel_ids = set(novel_df.index)
        # Write set of novel_ids to file
        with open(f'{filepath}-ids.txt', 'w') as file:
            file.write(str(novel_ids))

    def update_historic_set(self, novel_df):
        '''
        Updates the historic set with new identifiers and writes it back 
        to the historic file.

        Parameters:
            novel_df (pd.DataFrame): Data frame containing the novel entries, which are
            produced by applying the compare() method in this class to a data frame of recently
            scraped data.
        '''
        # Define novel_ids using indices from novel_df
        novel_ids = set(novel_df.index)

        with open(self.HISTORIC_IDS_FILEPATH, 'w') as file:
            self.historic_ids |= novel_ids
            file.write(str(self.historic_ids))


