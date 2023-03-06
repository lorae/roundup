
#url = "https://www.bea.gov/research/papers"
#x = "/html/body/div[1]/div[1]/div/section/div[2]/div/div/div[2]"
#open url
#for every element in the xpath x,
#(here are some example xpaths)
# /html/body/div[1]/div[1]/div/section/div[2]/div/div/div[2]/div[1]
# /html/body/div[1]/div[1]/div/section/div[2]/div/div/div[2]/div[2]
# /html/body/div[1]/div[1]/div/section/div[2]/div/div/div[2]/div[3]
#define the following:
        #Title = text contained in <h2 class="paper-title">
        #Link = href URL contained in <h2 class="paper-title">
        #Authors = text contained in <div class="paper-mod-date">
        #Date = text contained in <div class="paper-publication-date">
        #Number = text contained in <div class="views-field views-field-field-id paper-mod-date">
        #Abstract =
            #visit the link given by Link (above)
            #text given in this Xpath is the abstract: //*[@id="test"]/div[2]/article/div/div/div/div[1]
#repeat the above for every element in xpath x.
#Now construct a data frame "df" with the following columns:
#Title, Link, Date, Abstract, Author, Number

#save as a json file in
#"../processed_data/BEA.json")

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Define the URL and XPath
url = "https://www.bea.gov/research/papers"

# Initialize lists to store data
titles = []
links = []
authors = []
dates = []
numbers = []
abstracts = []

# Send a GET request to the URL and get the HTML content
response = requests.get(url)
html = response.content

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html, 'html.parser')

# Find all the elements matching the given XPath
elements = soup.select('div.view-content')

# Loop through each element and extract the data
for element in elements:
    # Extract the title and link
    title_tag = element.find('h2', {'class': 'paper-title'})
    title = title_tag.text.strip()
    link = title_tag.find('a')['href']
    
    # Append the base URL to the extracted link to get the full URL
    full_link = "https://www.bea.gov/" + link
    
    # Extract the author, date, and number
    author = element.find('div', {'class': 'paper-mod-date'}).text.strip()
    date = element.find('div', {'class': 'paper-publication-date'}).text.strip()
    number = element.find('div', {'class': 'views-field views-field-field-id paper-mod-date'}).text.strip()
    
    # Follow the link and extract the abstract
    link_response = requests.get(full_link)
    link_html = link_response.content
    link_soup = BeautifulSoup(link_html, 'html.parser')
    abstract = link_soup.find('p', {'class': 'card-abstract'}).get_text(strip=True)
    print(abstract)

    
    # Append the data to the respective lists
    titles.append(title)
    links.append(full_link)
    authors.append(author)
    dates.append(date)
    numbers.append(number)
    abstracts.append(abstract)

# Create a DataFrame from the extracted data
df = pd.DataFrame({
    'Title': titles,
    'Link': links,
    'Date': dates,
    'Abstract': abstracts,
    'Author': authors,
    'Number': numbers
})

# Save the DataFrame as a JSON file
df.to_json("../processed_data/BEA.json", orient='records', lines=True)

# Print the DataFrame
print(df.head())
