### ECB.py ###
# The purpose of this script is to scrape metadata from the most recent ECB working papers. This script uses
# the ECB RSS feed.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# Created: 3 Mar 2023

# NOTE: THIS SCRIPT IS NOT COMPLETE. It still needs the "Author" column.
# Unfortunately the solution is not straightforward. Either this code needs to be scrapped, and everything
# grabbed from the main working papers page
# https://www.ecb.europa.eu/pub/research/working-papers/html/index.en.html
# Or I can go for the author names as they appear in the PDF versions of the working paper. Unfortunately,
# they do not have landing pages for each paper, like I had hoped.

import feedparser
import pandas as pd

# Main code
URL = "https://www.ecb.europa.eu/rss/wppub.html"
f = feedparser.parse(URL)

data = [(# Title
         entry.title,
         # Link: note that this is for the PDF version, not the landing page
         entry.link,
         # Date
         entry.published,
         # Abstract
         entry.description,
         # Number: The paper number is contained in the "link" element. Spilt the url by the tilde ("~")
         # symbol, keeping the zero-th element. Then remove the leading element of the url. Only the paper
         # number remains.
         entry.link.split("~")[0].replace("https://www.ecb.europa.eu//pub/pdf/scpwps/ecb.wp", ""))
        #creates a tuple containing all of the above for the current entry
        for entry in f.entries]

# Create a pandas data frame from the extracted data
df = pd.DataFrame(data, columns=["Title", "Link", "Date", "Abstract", "Number"])
