### ECB.py ###
# The purpose of this script is to scrape metadata from the most recent ECB working papers. This script uses
# the ECB RSS feed.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# Created: 3 Mar 2023

import feedparser
import pandas as pd
import requests
import PyPDF2
import io
import re

# Extract data from RSS feed: Title, Link, Date, Abstract, Number
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

# Extract data from PDF file: Author
for i, row in df.iterrows():
    # Get the PDF content for the current row
    pdf_content = requests.get(row["Link"]).content
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))

    # Extract the text from the first page
    text = pdf_reader.pages[0].extract_text()

    # Clean up the text
        # Remove all instances of "\n" or two or more consecutive whitespace characters
        #with a single space character
    text = re.sub(r"(\n|\s{2,})", " ", text)
        # Remove the title from the text by replacing it with an empty string
    text = re.sub(re.escape(row["Title"]), "", text)
        # Remove the "Disclaimer" and anything following it from the text
    text = re.sub(r"Disclaimer.*", "", text)
        # Remove the string "Working Paper Series" from the text
    text = text.replace("Working Paper Series", "")

    # Remove any leading or trailing whitespace characters from the text
    text = text.strip()

    # Update the "Author" column in the DataFrame
    df.at[i, "Author"] = text

# Rearrange the columns of the DataFrame
df = df[["Title", "Link", "Date", "Abstract", "Author", "Number"]]

print(df)

# save the data frame to a JSON file
df.to_json('../processed_data/ECB.json', orient='records')
print("df saved to json")

# load the data frame from the JSON file
df_loaded = pd.read_json('../processed_data/ECB.json')
print("df_loaded loaded from json")

