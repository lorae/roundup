from src.scraper.sites.bea_scraper import BEAScraper
from src.scraper.sites.bfi_scraper import BFIScraper
from src.scraper.sites.bis_scraper import BISScraper
from src.scraper.sites.boe_scraper import BOEScraper
from src.scraper.sites.ecb_scraper import ECBScraper
from src.scraper.sites.fed_atlanta_scraper import FedAtlantaScraper

# List of scraper classes
scrapers = [BEAScraper, 
            BFIScraper,
            BISScraper,
            BOEScraper,
            ECBScraper,
            FedAtlantaScraper]  

# Progress bar 
total_tasks = len(scrapers)
for ScraperClass in scrapers:
    scraper_instance = ScraperClass()  # Instantiate the scraper
    print(f"scraping {scraper_instance.source} using {ScraperClass.__name__} ...")
    df = scraper_instance.fetch_and_process_data()  # Fetch and process data into standardized pandas df
    print(df) # Print output from scraper_instance.process_data()

'''if __name__ == "__main__":
    scraper = BFIScraper()  # Instantiate the scraper
    df = scraper.collect_data()  # Collect the data and process it into a pandas df
    print(df)'''