import feedparser
import pandas as pd
from ..generic_scraper import GenericScraper

class BISScraper(GenericScraper):
    def __init__(self):
        super().__init__("BIS")

    # Public method which is called from outside the class.
    def collect_data(self):
        # RSS feed URL
        url = 'https://www.bis.org/doclist/wppubls.rss?from=&till=&objid=wppubls&page=&paging_length=10&sort_list=date_desc&theme=wppubls&ml=false&mlurl=&emptylisttext='
        # Request and parse RSS feed contents
        f = feedparser.parse(url)

        data = {
            # Title
            'Title': [entry.title for entry in f.entries],
            # Link
            'Link': [entry.link for entry in f.entries],
            # Date
            'Date': [entry.date.split('T')[0] for entry in f.entries],
            # Abstract: "description" element contains both author and abstract, so grab the first element
            # after splitting the text by the line break ("<br />")
            'Abstract': [entry.description.split('<br />')[1] for entry in f.entries],
            # Author: "description" element contains both author and abstract, so grab the zero-th element
            # after splitting the text by the line break ("<br />"). Remove "by" from the string, then remove
            # leading and trailing spaces
            'Author': [entry.description.split('<br />')[0].replace('by', '') for entry in f.entries],
            # The paper number is contained in the "link" element. Remove the leading and trailing elements
            # of the URL.
            'Number': [entry.link.replace('https://www.bis.org/publ/work', '').replace('.htm', '') for entry in f.entries]
        }

        

        # Use the inherited process_data method to create and return the DataFrame
        return self.process_data(data)