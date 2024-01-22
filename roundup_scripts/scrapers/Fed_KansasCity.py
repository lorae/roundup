# Fed_KansasCity.py
# The purpose of this script is to scrape metadata from the most recent Kansas City Fed working papers,
# found at https://www.kansascityfed.org/research/research-working-papers/. This script uses xxx to do yyy.
#
# Lorae Stojanovic
#
# OpenAI's tool, ChatGPT, was used for coding assistance in this project.
# LE: 18 Jan 2024

import requests


def scrape():
    url = "https://www.kansascityfed.org/research/research-working-papers/research-working-paper-archive/"

    payload = {'csrfmiddlewaretoken': '',
    'archive-topics-search-input': '',
    'archive-authors-search-input': '',
    'archive-years': '2024',
    'archive-years': '2023',
    'archive-years-search-input': '',
    'sortby': 'date',
    'order': 'desc',
    'years': '2024;2023',
    'pageNumber': '1',
    'perPageCount': '50'}
    files=[

    ]
    headers = {
      'Accept': '*/*',
      'Accept-Language': 'en-US,en;q=0.9',
      'Connection': 'keep-alive',
      'Cookie': '',
      'Origin': 'https://www.kansascityfed.org',
      'Referer': 'https://www.kansascityfed.org/research/research-working-papers/research-working-paper-archive/',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-GPC': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

    
    

