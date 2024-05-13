import pandas as pd
import os
import ast
from datetime import datetime
import warnings


class HistoricDataComparer:
    '''
    A class to compare newly scraped data against a historical record set to identify novel entries.

    Attributes:
        historic_ids (set): Set of unique identifiers from previously observed data.

        current_datetime (str): Current date and time, formatted for file naming.

        current_date (str): Current date, formatted for data tagging.
    
    Constants:
        WP_IDS_FILEPATH (str): Filepath to the historic working paper identifiers. 
            This is where the historic registry of paper IDs is stored.

        WP_DATA_FILEPATH (str): Filepath to the historic working paper data. 
            This is where the titles, authors, abstracts, etc. of previously scraped working
             papers are stored.

        LOCAL_SCRAPE_OUTCOMES_FILEPATH (str): Filepath to the local scrape outcomes folder. 
            This is where the data and ids of newly scraped working papers are stored. This
            folder is for local debugging and web scraping use only. It is not read by
            other portions of the repository.
    '''
    # Class level constants 
    # File path to the historic working paper identifiers 
    WP_IDS_FILEPATH = 'data/wp_ids.txt'
    # File path to the historic working paper data  
    WP_DATA_FILEPATH = 'data/wp_data.csv' 
    # File path to the local scrape outcomes
    LOCAL_SCRAPE_OUTCOMES_FILEPATH = 'data/local_scrape_outcomes'  

    def __init__(self):
        '''
        Initializes the HistoricDataComparer. Loads the historic set of identifiers 
        from the file specified by WP_IDS_FILEPATH.
        '''
        # This attribute loads the contents of the historic working paper ids file,
        # which are stored as a Python sets
        self.historic_ids = self.load_historic_ids()
        # Defining current dates and times for use in save_local_results() and
        # compare() methods
        self.current_datetime = datetime.now().strftime('%Y-%m-%d-%H%M')
        self.current_date = datetime.now().strftime('%m/%d/%Y')

    def load_historic_ids(self):
        '''
        Loads the set of historical identifiers from the file specified by WP_IDS_FILEPATH.

        Returns:
            set: A set of strings representing historic identifiers.

        Raises:
            FileNotFoundError: If the file specified by WP_IDS_FILEPATH does not exist.
        '''
        try:
            with open(self.WP_IDS_FILEPATH, 'r') as file:
                return ast.literal_eval(file.read())
        except FileNotFoundError:
            raise FileNotFoundError(f'File {self.WP_IDS_FILEPATH} not found.')

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

    def save_local_results(self, novel_df):
        '''
        Saves the novel entries in .csv, .txt, and .html formats into the specified `LOCAL_SCRAPE_OUTCOMES_FILEPATH`.

        Note:
            Output files are saved in a directory specified by `LOCAL_SCRAPE_OUTCOMES_FILEPATH`, which 
            is typically configured to be ignored by version control (.gitignore). 
            This setup is intended for local debugging and temporary storage. 
            See README for more details.

        Parameters:
            novel_df (pd.DataFrame): Data frame containing the novel entries, which are
            produced by applying the compare() method in this class to a data frame of recently
            scraped data.

        Outputs:
            .csv: Contains all novel entries with metadata. File is saved in `LOCAL_SCRAPE_OUTCOMES_FILEPATH`
            directory with name `YYYY-MM-DD-HHMM-data.csv`.

            .html: Browser-viewable dashboard file with clickable links for each entry 
            title. File is saved in `LOCAL_SCRAPE_OUTCOMES_FILEPATH` directory with name 
            `YYYY-MM-DD-HHMM-dashboard.html`.

            .txt: Contains the set of unique identifiers of the novel entries, formatted 
            as a Python set for potential future debugging. File is saved in `LOCAL_SCRAPE_OUTCOMES_FILEPATH` 
            directory with name `YYYY-MM-DD-HHMM-ids.txt`.
        '''

        # Create a template filepath, which will be used to save the below
        # .csv, .html, and .txt files
        filepath = os.path.join(self.LOCAL_SCRAPE_OUTCOMES_FILEPATH, self.current_datetime)

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

    def append_ids_to_historic(self, novel_df):
        '''
        Appends newly scraped working paper identifiers to the historic 
        identifiers, then saves as a .txt file in `self.WP_IDS_FILEPATH`.
        File content is formatted as a Python set for easy retrieval and 
        comparison.

        Parameters:
            novel_df (pd.DataFrame): Data frame containing the novel entries, which are produced by applying the compare() method in this class to a data frame of recently
            scraped data.
        '''
        # Define novel_ids using indices from novel_df
        novel_ids = set(novel_df.index)

        with open(self.WP_IDS_FILEPATH, 'w') as file:
            self.historic_ids |= novel_ids
            file.write(str(self.historic_ids))

    def append_data_to_historic(self, novel_df):
        '''
        Appends newly scraped working paper rows - containing Title, Author, Link,
        Date, Link, Number, Abstract, estPubDate, Source, and unique identifier 
        index - to the historic data. Saves as a .csv file in 
        `self.WP_DATA_FILEPATH`.

        Parameters:
            novel_df (pd.DataFrame): Data frame containing the novel entries, which are
            produced by applying the compare() method in this class to a data frame of recently
            scraped data.
        '''
        try:
            # Read in the existing historic data
            existing_df = pd.read_csv(self.WP_DATA_FILEPATH)
            print("existing_df read")
            # Map the column order of historic data to column_order variable
            column_order = existing_df.columns.tolist()
            print("column order mapped")
            # Apply the column order to novel_df
            novel_df = novel_df[column_order]
            print("column order applied to novel_df")
            # Append novel_df rows to csv file self.WP_DATA_FILEPATH
            novel_df.to_csv(self.WP_DATA_FILEPATH, mode='a', header=False, index=False, encoding='utf-8-sig')
            print("csv written")
        except FileNotFoundError: 
            # If file not found, write a new file
            novel_df.to_csv(self.WP_DATA_FILEPATH, mode='w', header=True, index=False, encoding='utf-8-sig')
            warnings.warn(f'No existing file found at {self.WP_DATA_FILEPATH}. New file created.')

