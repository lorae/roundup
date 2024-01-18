# Fed_KansasCity.py
# The purpose of this script is to scrape metadata from the most recent Kansas City Fed working papers,
# found at https://www.kansascityfed.org/research/research-working-papers/. This script uses xxx to do yyy.
#
# Lorae Stojanovic
#
# OpenAI's tool, ChatGPT, was used for coding assistance in this project.
# LE: 18 Jan 2024

def scrape():
    url = "https://www.kansascityfed.org/research/research-working-papers/"
    print(url)
    
    # Get the soup
    soup = get_soup(url)
    print(soup)