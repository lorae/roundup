import feedparser
from ..generic_scraper import GenericScraper

class BISScraper(GenericScraper):
    def __init__(self):
        super().__init__(source = "BIS")

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
        url = 'https://www.bis.org/doclist/wppubls.rss?from=&till=&objid=wppubls&page=&paging_length=10&sort_list=date_desc&theme=wppubls&ml=false&mlurl=&emptylisttext='
        # Request and parse RSS feed contents
        f = feedparser.parse(url)

        data = []
        for entry in f.entries:
            title = entry.title
            link = entry.link
            date = entry.date.split('T')[0]
            # Abstract: "description" element contains both author and abstract, so grab the first element
            # after splitting the text by the line break ("<br />")
            abstract = entry.description.split('<br />')[1]
            # Author: "description" element contains both author and abstract, so grab the zero-th element
            # after splitting the text by the line break ("<br />"). Remove "by" from the string, then remove
            # leading and trailing spaces
            author = entry.description.split('<br />')[0].replace('by', '')
            # The paper number is contained in the "link" element. Remove the leading and trailing elements
            # of the URL.
            number = entry.link.replace('https://www.bis.org/publ/work', '').replace('.htm', '')
            
            # Append title, link, date, abstract, author, and number to the
            # `data` dictionary list
            data.append({
                'Title': title,
                'Link': link,
                'Date': date,
                'Abstract': abstract,
                'Author': author,
                'Number': number
            })

        return data