### BEA.py ###
# The purpose of this script is to scrape metadata from the most recent BEA working papers. This script uses
# the BEA research papers landing page (given by the URL below). Abstracts are found on the specific landing
# pages corresponding to each individual paper.
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# Created: 5 Mar 2023

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL
url = "https://www.bea.gov/research/papers"

# Send a GET request to the URL and get the HTML content
html = requests.get(url).content

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html, 'html.parser')

# Find all the elements matching the given XPath
elements = soup.select('div.view-content div.card')

# Extract the data from each element and store it in a list of dictionaries
data = []
for element in elements:
    data.append({
        'Title': element.find('h2', {'class': 'paper-title'}).text.strip(),
        'Link': "https://www.bea.gov/" + element.find('h2', {'class': 'paper-title'}).find('a')['href'],
        'Author': element.find('div', {'class': 'paper-mod-date'}).text.strip(),
        'Date': element.find('div', {'class': 'paper-publication-date'}).text.strip().replace('Published', ''),
        'Number': element.find('div', {'class': 'views-field views-field-field-id paper-mod-date'}).text.strip(),
        'Abstract': BeautifulSoup(requests.get("https://www.bea.gov/" + element.find('h2', {'class': 'paper-title'}).find('a')['href']).content, 'html.parser').find('p', {'class': 'card-abstract'}).get_text(strip=True)
    })

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)

# Save the DataFrame as a JSON file
df.to_json("../processed_data/BEA.json", orient='records', lines=True)

# Print the DataFrame
print(df)
