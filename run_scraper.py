from src.scraper.sites.bea_gov import BEAScraper

if __name__ == "__main__":
    scraper = BEAScraper()  # Instantiate the scraper
    df = scraper.collect_data()  # Collect the data and process it into a DataFrame
    print(df)  # Print the DataFrame to see the result