from src.scraper.sites.bea_scraper import BEAScraper
from src.scraper.sites.bfi_scraper import BFIScraper
from src.scraper.sites.bis_scraper import BISScraper
from src.scraper.sites.boe_scraper import BOEScraper

# List of scraper classes
scrapers = [BEAScraper, 
            BFIScraper,
            BISScraper,
            BOEScraper]  

# Progress bar 
total_tasks = len(scrapers)
for ScraperClass in scrapers:
    # Append the result of each scrape to the list
    print(f"running {ScraperClass} ...")
    scraper = ScraperClass()  # Instantiate the scraper
    df = scraper.collect_data()  # Collect the data and process it into a pandas df
    print(df)

'''if __name__ == "__main__":
    scraper = BFIScraper()  # Instantiate the scraper
    df = scraper.collect_data()  # Collect the data and process it into a pandas df
    print(df)'''