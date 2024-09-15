import os
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
from typing import Dict, Any


def request_soup(session_args: requests.Request) -> BeautifulSoup:
    '''
    Requests an arbitrary remote resource using the provided `Request`-formatted object and 
    parses it using BeautifulSoup.

    :param session_args : Requests-formatted session arguments.
    :type session_args: requests.Request
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

    # Determine if running in GitHub Actions by checking for the environment variable
    if 'GITHUB_ACTIONS' in os.environ:
        # Use the pre-installed chromedriver path from environment variable
        chrome_driver_path = os.environ.get('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
    else:
        # Install ChromeDriver using webdriver_manager for local environment
        chrome_driver_path = ChromeDriverManager().install()

        # Due to a recent update in webdriver_manager, the ChromeDriver path may incorrectly point to a 
        # non-executable file ('THIRD_PARTY_NOTICES.chromedriver') instead of the actual 'chromedriver.exe'.
        # The following check ensures that the path is corrected to point to the executable.
        if chrome_driver_path.endswith("THIRD_PARTY_NOTICES.chromedriver"):
            chrome_driver_path = chrome_driver_path.replace(
                "THIRD_PARTY_NOTICES.chromedriver", "chromedriver.exe"
            )

    print(f"Using ChromeDriver at: {chrome_driver_path}")  # Debugging line to check path

    # Set up ChromeDriver service
    chrome_service = Service(chrome_driver_path)
    
    # Set up Chrome options
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

    # Initialize WebDriver with the service and options
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


def request_json(method: str, 
                 url: str, 
                 headers: Dict[str, str], 
                 data: Dict[str, Any] = None, 
                 files: Dict[str, Any] = None,
                 params: Dict[str, Any] = None) -> Dict[str, Any]:
    '''
    Makes an HTTP request to a specified URL with the given method, headers, data, files, 
    and query parameters, and returns the parsed JSON response.

    :param method: HTTP method to use ('GET', 'POST', etc.).
    :param url: URL to make the request to.
    :param headers: HTTP headers to include in the request.
    :param data: Data to send in the body of the request. Used for 'POST' and 'PUT' methods. Default is None.
    :param files: Files to send in the multipart request. Used for 'POST' and 'PUT' methods. Default is None.
    :param params: Query parameters to append to the URL. Used for 'GET' requests. Default is None.
    :type method: str
    :type url: str
    :type headers: Dict[str, str]
    :type data: Dict[str, Any]
    :type files: Dict[str, Any]
    :type params: Dict[str, Any]
    :raises HTTPError: If the response status code is not 200.
    :return: JSON object containing the response data.
    '''
    response = requests.request(method, url, headers=headers, data=data, files=files, params = params)
    
    # Check if the response status code is 200 (OK)
    if response.status_code != 200:
        raise requests.HTTPError(f'Error: Received status code {response.status_code} for URL: {response.url}', response=response)
    
    # Parse and return the JSON from the response
    return response.json()
