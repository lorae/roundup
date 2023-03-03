### IMF.py ###
# The purpose of this script is to scrape metadata from the most recent IMF working papers
# from the IMF website.
# This paper uses the IMF RSS feed.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# Created: 2 Mar 2023

### this code needs a lot of work.

import requests
from bs4 import BeautifulSoup
import feedparser
import pandas as pd
from lxml import html

# Define functions
def get_element_text(url, xpath):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    elems = tree.xpath(xpath)
    if isinstance(elems, list):
        return ''.join([elem.text_content().strip() for elem in elems])
    elif elems is not None:
        return elems.text.strip()
    else:
        return None


def get_abstracts(df):
    return [get_element_text(link, '/html/body/div[3]/main/article/div[1]/div/section[1]/p[8]/text()')
            for link in df['Link']]

def get_authors(df):
    return [[author.text for author in BeautifulSoup(requests.get(link).content, 'html.parser').select_one('p.pub-desc.hide').find_all('a')]
            for link in df['Link']]

def get_numbers(df):
    return [get_element_text(link, '/html/body/div[3]/main/article/div[1]/div/section[3]/div/p[6]')
            for link in df['Link']]

# Main code
URL = "https://www.imf.org/en/Publications/RSS?language=eng&series=IMF%20Working%20Papers"
f = feedparser.parse(URL)

data = [(entry.title,
         entry.link,
         entry.published) # creates a tuple containing the title, link, publication date, and summary for the current entry
        for entry in f.entries]

df = pd.DataFrame(data, columns=["Title", "Link", "Date"])

df["Abstract"] = get_abstracts(df)
df["Author"] = get_authors(df)
df["Number"] = get_numbers(df)

print(df)

# save the data frame to a JSON file
df.to_json('../processed_data/IMF.json', orient='records')
print("df saved to json")

# load the data frame from the JSON file
df_loaded = pd.read_json('../processed_data/IMF.json')
print("df_loaded loaded from json")
