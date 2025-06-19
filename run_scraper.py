import traceback
import sys
import pandas as pd
from src.data_comparer import HistoricDataComparer

from src.scraper.sites.bea_scraper import BEAScraper
from src.scraper.sites.bfi_scraper import BFIScraper
from src.scraper.sites.bis_scraper import BISScraper
from src.scraper.sites.boe_scraper import BOEScraper
from src.scraper.sites.ecb_scraper import ECBScraper
from src.scraper.sites.fed_atlanta_scraper import FedAtlantaScraper
from src.scraper.sites.fed_board_notes_scraper import FedBoardNotesScraper
from src.scraper.sites.fed_board_scraper import FedBoardScraper
from src.scraper.sites.fed_boston_scraper import FedBostonScraper
from src.scraper.sites.fed_chicago_scraper import FedChicagoScraper
from src.scraper.sites.fed_cleveland_scraper import FedClevelandScraper
from src.scraper.sites.fed_dallas_scraper import FedDallasScraper
from src.scraper.sites.fed_kansas_city_scraper import FedKansasCityScraper
from src.scraper.sites.fed_minneapolis_scraper import FedMinneapolisScraper
from src.scraper.sites.fed_new_york_scraper import FedNewYorkScraper
from src.scraper.sites.fed_san_francisco_scraper import FedSanFranciscoScraper
from src.scraper.sites.fed_philadelphia_scraper import FedPhiladelphiaScraper
from src.scraper.sites.fed_richmond_scraper import FedRichmondScraper
from src.scraper.sites.fed_st_louis_scraper import FedStLouisScraper
from src.scraper.sites.imf_scraper import IMFScraper
from src.scraper.sites.nber_scraper import NBERScraper

# List of scraper classes
scrapers = [
            BEAScraper, 
            BFIScraper,
            BISScraper,
            BOEScraper,
            ECBScraper,
            FedAtlantaScraper,
            FedBoardNotesScraper,
            FedBoardScraper,
            FedBostonScraper,
            FedChicagoScraper,
            FedClevelandScraper,
            FedDallasScraper,
            FedKansasCityScraper,
            FedMinneapolisScraper,
            FedNewYorkScraper,
            FedSanFranciscoScraper,
            FedPhiladelphiaScraper,
            FedRichmondScraper,
            FedStLouisScraper,
            IMFScraper,
            NBERScraper
            ]

########## Part 1: Scraping Data ##########
print(f'--------------------\n Part 1: Data Scrape \n--------------------')

# Progress counters
total_tasks = len(scrapers)
attempted = 0
succeeded = 0

# Initialize an empty list to hold all data frames from individual
# scrapes
dfs = []

# Loop through each scraper class and instantiate
for ScraperClass in scrapers:
    scraper_instance = ScraperClass()
    
    # 'try' and 'except' syntax allows an instance of all scraper 
    # classes to be attempted, even if some fail. 
    try:
        print(f'Scraping {scraper_instance.source} using {ScraperClass.__name__} ...')
        df = scraper_instance.fetch_and_process_data()
        if df is not None:

            # Append the new df to dfs
            dfs.append(df)
            print(df)

            # Update succeeded counter
            succeeded += 1

            # Update scraper status
            scraper_instance.update_scraper_status(source = scraper_instance.source, 
                                                   is_successful = True, 
                                                   filename='streamlit/scraper_status.txt')
            print(f"{scraper_instance.source} scraped successfully.")
        else:
            raise Exception("No data returned")
    
    except Exception as e:
        print(f'Error with {ScraperClass.__name__}: {str(e)}')
        
        # Update succeeded counter (or, in this case, don't: the 
        # attempt failed)
        succeeded += 0

        # Update scraper status
        scraper_instance.update_scraper_status(source = scraper_instance.source, 
                                                   is_successful = False, 
                                                   filename='streamlit/scraper_status.txt')

        # Print the full traceback
        traceback.print_exc()

    # Update attempted counter
    attempted += 1

    # Print progress message
    print(
        f'\n{attempted} of {total_tasks} tasks attempted. {succeeded} of {total_tasks} tasks succeeded.'
        f'\n----------------------------------------'
        )
    
# Combine all data frames in df into one large data frame
# If dfs nonempty, concatenate all data frames in the list dfs into a single data frame.
# If dfs empty, terminate script with error code 1.
print('Concatenating all newly scraped data into one data frame...')

if dfs:  # This will be True if dfs is not empty
    df = pd.concat(dfs, ignore_index=False) # Purposefully keep indices
    print(df)
else:
    print('No data frames to concatenate. dfs is empty. Script terminating.')
    sys.exit(1)

# Part 2: Comparing to historical data
print(f'--------------------\n Part 2: Comparing to Historical Data \n--------------------')

# Instantiate the HistoricDataComparer class
comparer = HistoricDataComparer()
print('HistoricDataComparer class instantiated.')

# Use the compare method within the HistoricDataComparer class to
# determine which of the data in `df` is novel. Save these entries
# in novel_df
novel_df = comparer.compare(df)
print('novel_df: ')
print(novel_df)

if not novel_df.empty: # If novel entries exist...
    # ...Save them locally
    comparer.save_local_results(novel_df = novel_df)
    # ...Append the newly scraped ids the historic set of ids
    comparer.append_ids_to_historic(novel_df = novel_df)
    print(f'Historic set updated in {comparer.WP_IDS_FILEPATH}')
    # ...Append the newly scraped data rows to the historic data table
    comparer.append_data_to_historic(novel_df = novel_df)
    print(f'Results saved in {comparer.WP_DATA_FILEPATH}')

print(f'--------------------\n Script has completed running. \n--------------------')

