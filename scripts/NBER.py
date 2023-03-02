# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 2 Mar 2023

import requests
import re
import json
import pandas as pd
from lxml import html

url = 'https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=100'
response = requests.get(url)
data = json.loads(response.text)

titles = [paper['title'] for paper in data['results']]
authors_htmls = [paper['authors'] for paper in data['results']]
authors = [[re.sub('<[^>]+>', '', author) for author in authors_html] for authors_html in authors_htmls]
published_dates = [paper['displaydate'] for paper in data['results']]
abstracts = [paper['abstract'] for paper in data['results']]
urls = ["https://www.nber.org" + paper['url'] for paper in data['results']]
numbers = [url.split('/papers/w')[1] for url in urls]

long_abstracts = []
for url in urls:
    page = requests.get(url)
    tree = html.fromstring(page.content)
    long_abstract = tree.xpath('/html/body/div[2]/main/div[2]/div[2]/div/p/text()')[0].strip()
    long_abstracts.append(long_abstract)

df = pd.DataFrame({
    'Title': titles,
    'Authors': authors,
    'Published Date': published_dates,
    'Abstract': abstracts,
    'URL': urls,
    'Number': numbers,
    'Long Abstract': long_abstracts
})

df = df.sort_values(by=['Number'])
print(df)
