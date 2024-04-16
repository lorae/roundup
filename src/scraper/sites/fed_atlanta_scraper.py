from ..generic_scraper import GenericScraper
import feedparser
import calendar

class FedAtlantaScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = 'FED-ATLANTA')

    # Public method which is called from outside the class.
    def fetch_data(self):
        '''
        Requests and parses the source's main RSS feed using feedparser
        to get title, link, author, date, number, and abstract for
        each working paper entry.

        :return: A list of dictionaries containing Title, Author, Link, 
        Abstract, Number and Date for each working paper entry 
        :rtype: list
        '''
        # RSS feed URL
        url = "https://www.atlantafed.org/rss/wps"
        # Request and parse RSS feed contents
        f = feedparser.parse(url)

        # Initialize output `data`
        data = []
        for entry in f.entries:
            title = entry.title

            link = entry.link

            # The date is the published entry, minus 11 characters (indicating hour, minute, and time zone)
            date = entry.published[:-10].strip()
            # The last 4 chars of date comprise the year (helper variable)
            year = date[-4:] # year is a helper variable
            mon = date[-8:-5] # mon is a helper variable (3-letter month name)
            # helper variable
            month_year = calendar.month_name[list(calendar.month_abbr).index(mon)] + " " + year 

            # The abstract is the 1st element of "description", after splitting it by the 
            # name of the month and year the paper was published. This is because the
            # "desciption" also contains author and working paper number. This was the
            # simplest way I could find to isolate the abstract without navigating to different
            # URLs.
            abstract = entry.description.split(f"{month_year}")[1]

            # The number is the middle element of "description", after splitting it by the
            #  string "Working Paper" and by the month_year string.
            number = entry.description.split("Working Paper ")[1].split(f"{month_year}")[0].strip()

            # The author is the first element of "description", the part that appears just
            # before the string "Working Paper".
            author = entry.description.split("Working Paper")[0].strip()

            # Append title, link, date, abstract, number, and author
            # `data` dictionary list
            data.append({'Title': title,
                    'Link': link,
                    'Date': date,
                    'Abstract': abstract,
                    'Number': number,
                    'Author': author
                    })
            
        return data