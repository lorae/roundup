# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 2 Mar 2023

import requests
import re
import json

url = 'https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=100'
response = requests.get(url)
data = json.loads(response.text)

title = data['results'][0]['title']
authors_html = data['results'][0]['authors']
authors = [re.sub('<[^>]+>', '', author) for author in authors_html]
published_date = data['results'][0]['displaydate']
abstract = data['results'][0]['abstract']
url = "https://www.nber.org" + data['results'][0]['url']
number = url.split('/papers/w')[1] # extract the paper number

print(title)
print(authors)
print(published_date)
print(abstract)
print(url)
print(number)
