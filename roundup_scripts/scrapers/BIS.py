### BIS.py ###
# The purpose of this script is to scrape metadata from the most recent BIS working papers. This script uses
# the BIS RSS feed.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# Created: 3 Mar 2023

import feedparser
import pandas as pd

# Main code
URL = 'https://www.bis.org/doclist/wppubls.rss?from=&till=&objid=wppubls&page=&paging_length=10&sort_list=date_desc&theme=wppubls&ml=false&mlurl=&emptylisttext='
f = feedparser.parse(URL)

data = [(# Title
         entry.title,
         # Link
         entry.link,
         # Date
         entry.date,
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
print("BIS titles, links, dates, abstracts, authors, and numbers have been gathered.")

print(df)

# save the data frame to a JSON file
df.to_json('../processed_data/BIS.json', orient='records')
print("df saved to json")

# load the data frame from the JSON file
df_loaded = pd.read_json('../processed_data/BIS.json')
print("df_loaded loaded from json")
