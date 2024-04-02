from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


def request_soup(session_args: requests.Request) -> BeautifulSoup:
    '''
    Requests an arbitrary remote resource using the provided `Request`-formatted object and 
    parses it using BeautifulSoup.

    :param sessionArgs : Requests-formatted session arguments.
    :raises HTTPError: If the response status code is not 200.
    :return: BeautifulSoup object containing the parsed page source.
    '''

    session = requests.Session()
    prepared_request = session.prepare_request(session_args)
    response: requests.Response = session.send(prepared_request)

    # Check if the status code is not 200
    if response.status_code != 200:
        # Raise an HTTPError if the status is not 200
        raise HTTPError(f'Error: Received status code {response.status_code} for URL: {response.url}', response=response)
    
    # Parse using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup

def selenium_soup(url: str) -> BeautifulSoup:
    '''
    Fetches a webpage using Selenium WebDriver and returns its content parsed by BeautifulSoup.
    
    :param url: URL of the webpage to fetch.
    :return: BeautifulSoup object containing the parsed page source.
    '''

    chrome_service = Service(ChromeDriverManager().install())
    
    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]
    for option in options:
        chrome_options.add_argument(option)

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get(url)  # Go to the page
    time.sleep(5)  # Pause to allow the page to fully load
    
    # Use WebDriverWait to wait for a specific element to become available
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "snippet1"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)
    except Exception as e:
        print(f"An error occurred while waiting for element: {e}")
    time.sleep(5)  # Additional pause after scrolling

    soup = BeautifulSoup(driver.page_source, 'html.parser')  # Parse page source with BeautifulSoup
    driver.quit()  # Close the WebDriver

    return soup