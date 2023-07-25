# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 21 Jun 2023

import requests
import re
import json
import pandas as pd
from lxml import html


def scrape():
    # Define the URL for the NBER working papers API
    URL = 'https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=100'

    # Make a GET request to the NBER API and parse the JSON response into a Python dictionary
    data = json.loads(requests.get(URL).text)['results']

    # Create a Pandas DataFrame from the extracted data, with the "Long Abstract" extracted from the paper's URL using XPath
    df = pd.DataFrame({
        'Title': [d['title'] for d in data],
        'Link': ['https://www.nber.org' + d['url'] for d in data],
        'Date': [d['displaydate'] for d in data],
        'Abstract': [html.fromstring(requests.get('https://www.nber.org' + d['url']).content)
                          .xpath('/html/body/div[2]/main/div[2]/div[2]/div/p/text()')[0].strip()
                          for d in data],    
        'Author': [[re.sub('<[^>]+>', '', author) for author in d['authors']] for d in data],
        'Number': [d['url'].split('/papers/w')[1] for d in data]
    }).sort_values(by='Number')

    # Instead of the data frame having row names (indices) equalling 1, 2, etc,
    # we set them to be an identifier that is unique. In the case of NBER, we combine
    # NBER with the number of the paper (eg. 999) to get an identifier NBER999 that
    # is completely unique across all papers scraped.
    df.index = "NBER" + df['Number'].astype(str)
    df.index.name = None
    
    print(df)
    return(df)

'''
# Save the DataFrame to a JSON file
df.to_json('processed_data/NBER.json')
print("df saved to json")

# load the data frame from the JSON file
df_loaded = pd.read_json('processed_data/NBER.json')
print("df_loaded loaded from json")
'''

# Print the DataFrame to the console
# Only un-comment this line to print df in long format. Otherwise will print in short format
'''
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.expand_frame_repr', False, 'display.max_colwidth', -1):
    print(df)
'''

#print(df_loaded)

# Only un-comment this line for troubleshooting purposes
# load to a CSV to check if it looks good
# df_loaded.to_csv('output.csv')

'''
# Make a historical file by taking just the less recent entries and saving
historic_NBER = df_loaded.head(60)
historic_NBER.to_json('historic_data/NBER.json', orient='records')
'''
