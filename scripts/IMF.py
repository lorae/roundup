# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 2 Mar 2023


### this code needs a lot of work.

import requests
from bs4 import BeautifulSoup
import re

# Define functions
def get_abstract(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.select_one("#issueDisclaimer~ .pub-desc").text.strip().replace("\n", "")

def get_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    nodes = soup.select(".pub-row")

    titles = [node.select_one("h6 a").text.strip() for node in nodes]
    authors = [re.sub("Author:|\r\n", "", node.select_one(".author").text).strip().replace("; ", ";") for node in nodes]
    dates = [re.sub("Date: ", "", node.select_one("p:nth-child(4)").text.strip()) for node in nodes]
    links = ["https://www.imf.org" + node.select_one("h6 a")["href"] for node in nodes]

    return {
        "Title": titles,
        "Authors": authors,
        "Date": dates,
        "Link": links
    }

# Main code
##this should be the main link:
#https://www.imf.org/en/Publications/Search?#sort=relevancy&numberOfResults=50&f:series=[WRKNGPPRS]
url = 'https://www.imf.org/en/publications/search?when=After&series=IMF+Working+Papers'
imf_urls = [f"{url}&page={page_num}" for page_num in range(1, 6)]
imf_htmls = [requests.get(url).content for url in imf_urls]

abstracts = [get_abstract(url) for url in imf_urls]
data = [get_data(url) for url in imf_urls]

# Combine data and abstracts into a single list of dictionaries
for i in range(len(data)):
    for j in range(len(data[i]["Title"])):
        data[i][j]["Abstract"] = abstracts[i][j]

# Convert list of dictionaries to pandas DataFrame
import pandas as pd
df = pd.concat([pd.DataFrame(d) for d in data], ignore_index=True)

# Save DataFrame to JSON file
df.to_json("processed_data/IMF.json")
