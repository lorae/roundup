from src.scraper.sites.bea_scraper import BEAScraper
from src.scraper.sites.bfi_scraper import BFIScraper
from src.scraper.sites.bis_scraper import BISScraper
from src.scraper.sites.boe_scraper import BOEScraper
from src.scraper.sites.ecb_scraper import ECBScraper
from src.scraper.sites.fed_atlanta_scraper import FedAtlantaScraper
from src.scraper.sites.fed_board_notes_scraper import FedBoardNotesScraper
from src.scraper.sites.fed_board_scraper import FedBoardScraper
from src.scraper.sites.fed_boston_scraper import FedBostonScraper
# fed chicago

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
            FedBostonScraper
            ]

# Progress bar 
total_tasks = len(scrapers)
i = 1 # counter

# Loop through each scraper class and instantiate
for ScraperClass in scrapers:
    # Instantiate the scraper
    scraper_instance = ScraperClass()  
    print(f'scraping {scraper_instance.source} using {ScraperClass.__name__} ...')
    df = scraper_instance.fetch_and_process_data()  # Fetch and process data into standardized pandas df
    print(df) # Print output from scraper_instance.process_data()
    print(f'{scraper_instance.source} scraped. {i} of {total_tasks} tasks complete.')
    print('----------')
    i += 1 #update counter

'''if __name__ == "__main__":
    scraper = BFIScraper()  # Instantiate the scraper
    df = scraper.collect_data()  # Collect the data and process it into a pandas df
    print(df)'''