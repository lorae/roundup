# Fed_Boston.py
# The purpose of this script is to scrape metadata from the most recent Boston Fed working papers. This script uses
# the Boston Fed's Working Paper landing page.
# Lorae Stojanovic
#
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 21 Aug 2023

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_soup(url): 
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    # Go to the page
    driver.get(url)

    # Wait for the button with the specific aria-label and then click it
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="2023 Series"]'))
    )
    button.click()

    # If you need to wait for some elements to ensure the page has loaded after clicking, 
    # you can use WebDriverWait. For now, I'll add a simple wait to check for page complete loading.
    WebDriverWait(driver, 30).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete'
    )

    # Get the page source and parse it
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Don't forget to close the driver
    driver.quit()

    return soup
    
url = "https://www.bostonfed.org/publications/research-department-working-paper/"
soup = get_soup(url)
#print(soup)

elements = soup.find_all('div', {'class': 'event-list-item'})
print(elements)
