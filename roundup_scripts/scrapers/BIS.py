### BIS.py ###
# The purpose of this script is to scrape metadata from the most recent BIS working papers. This script uses
# the BIS RSS feed.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# Created: 3 Mar 2023

import feedparser
import pandas as pd

# I define the function "scrape" in every webscraper. That way, in runall.py, it is easy to call BOE.scrape()
# or NBER.scrape(), for instance, knowing that they all do the same thing - namely, navigate to their respective 
# websites and extract the data.
def scrape():
     # Let's start by going to the RSS feed and extracting the data
    URL = 'https://www.bis.org/doclist/wppubls.rss?from=&till=&objid=wppubls&page=&paging_length=10&sort_list=date_desc&theme=wppubls&ml=false&mlurl=&emptylisttext='
    f = feedparser.parse(URL)

    data = [(# Title
             entry.title,
             # Link
             entry.link,
             # Date
             entry.date.split("T")[0],
             # Abstract: "description" element contains both author and abstract, so grab the first element
             # after splitting the text by the line break ("<br />")
             entry.description.split("<br />")[1],
             # Author: "description" element contains both author and abstract, so grab the zero-th element
             # after splitting the text by the line break ("<br />"). Remove "by" from the string, then remove
             # leading and trailing spaces
             entry.description.split("<br />")[0].replace("by", ""),
             # The paper number is contained in the "link" element. Remove the leading and trailing elements
             # of the URL.
             entry.link.replace("http://www.bis.org/publ/work", "").replace(".htm", "")) # number
            #creates a tuple containing all of the above for the current entry
            for entry in f.entries]

    # Create a pandas data frame from the extracted data
    df = pd.DataFrame(data, columns=["Title", "Link", "Date", "Abstract", "Author", "Number"])
    #print("BIS titles, links, dates, abstracts, authors, and numbers have been gathered.")

    # Instead of the data frame having row names (indices) equalling 1, 2, etc,
    # we set them to be an identifier that is unique. In the case of BOE, we combine
    # BOE with the number of the paper (eg. 999) to get an identifier BOE999 that
    # is completely unique across all papers scraped.
    df["Source"] = "BIS"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None
    
    print(df)
    return(df)

