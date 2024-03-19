# The website is active!

View it here: https://roundup.streamlit.app/

# About

The purpose of this project is regularly track and present the most recent working papers in economics. ('Working papers', also known as 'pre-print' papers, present academic research that has not yet been peer-reviewed.) Remotely run via GitHub Actions once daily, this project scrapes data from 20 different websites at 6:40 AM EST, compares newly collected data to a historic database of working papers, and presents only the most recent ones on the [project dashboard](https://roundup.streamlit.app/). The dashboard may be of use for those interested in understanding the most recent active areas of economics research, such as economists, policy-oriented researchers, and students. As of February 2024, the project incorporates data from 20 different sources.

# How it works

The web scrapers in this project gather six pieces of information on each economics working paper:
- Title
- Authors
- Abstract
- Date published (If it was posted and re-posted, the most recent date of publication is used.)
- URL
- Paper ID number (according to each website's own numbering system)

Each website has a bespoke module, located in `roundup-scripts/scrapers`. When the GitHub Actions project workflow, `.github/workflows/main.yml` is activated at 6:40 AM EST every morning, it runs the main python script of the project - `runall.py` - which cycles through each of the 20 web scraping modules. After the data are collected, it runs `roundup_scripts/compare.py`, which compares the recently-gathered data to a set of working papers already seen. All those that are truly novel are assigned an estimated publication date of the day that they were first identified, and appended to the `historic/papers-we-have-seen-metadata` file.

The `streamlit_app.py` script produces the [project dashboard](https://roundup.streamlit.app/), which is a user-friendly aggregation of the most recent economics research. The app draws primarily from the `historic/papers-we-have-seen-metadata` file to populate itself with information.

The purpose of this repository is to maintain and improve the [project dashboard](https://roundup.streamlit.app/). The `runall.py` script and its underlying web scrapers are run remotely using a GitHub Actions. However, the repo may also be run locally on your personal computer. Instructions for local setup may be found in the `Getting Started` section of this document.

# Data sources
Websites that are scraped for data, as of February 2024, are:

| Name of website                                                  | Name of script                          | Scraping method |
|------------------------------------------------------------------|-----------------------------------------|-----------------|
| [Bureau of Economic Analysis](https://www.bea.gov/research/papers)                                      | roundup_scripts/scrapers/BEA.py         | Scrapes main landing page and each individual WP's landing page using Requests and BeautifulSoup           |
| [Becker Friedman Institute](https://www.bea.gov/research/papers) (at the University of Chicago)       | roundup_scripts/scrapers/BFI.py         | Scrapes main landing page and each individual WP's landing page using Requests and BeautifulSoup         |
| [Bank for International Settlements](https://www.bis.org/doclist/wppubls.rss?from=&till=&objid=wppubls&page=&paging_length=10&sort_list=date_desc&theme=wppubls&ml=false&mlurl=&emptylisttext=)                                | roundup_scripts/scrapers/BIS.py         | Scrapes RSS feed using Feedparser     |
| [Bank of England](https://www.bankofengland.co.uk/rss/publications)                                                  | roundup_scripts/scrapers/BOE.py         | Scrapes RSS feed using Feedparser and each individual WP's landing page using Requests and BeautifulSoup           |
| [European Central Bank](https://www.ecb.europa.eu/pub/research/working-papers/html/index.en.html)                                            | roundup_scripts/scrapers/ECB.py         | Reads main landing page using a headless instance of Chrome via Selenium, and parses using BeautifulSoup          |
| [Federal Reserve Bank of Atlanta](https://www.atlantafed.org/rss/wps)                                 | roundup_scripts/scrapers/Fed_Atlanta.py     | Scrapes RSS feed using Feedparser             |
| [Federal Reserve Board of Governors](https://www.federalreserve.gov/econres/feds/index.htm) (of the United States): working papers | roundup_scripts/scrapers/Fed_Board.py       | Scrapes main landing page using Requests and BeautifulSoup             |
| [Federal Reserve Board of Governors](https://www.federalreserve.gov/econres/notes/feds-notes/default.htm) (of the United States): Fed Notes | roundup_scripts/scrapers/Fed_Board_Notes.py       | Scrapes main landing page using Requests and BeautifulSoup             |
| [Federal Reserve Bank of Boston](https://www.bostonfed.org/publications/research-department-working-paper/)                               | roundup_scripts/scrapers/Fed_Boston.py     | Reads main landing page using a headless instance of a Chrome via Selenium and parses with BeautifulSoup. Extracts data from each individual WP's landing page using Requests and BeautifulSoup and reads PDF metadata using PyPDF2 and io       |
| [Federal Reserve Bank of Chicago](https://www.chicagofed.org/publications/publication-listing?filter_series=18)                                | roundup_scripts/scrapers/Fed_Chicago.py     | Scrapes main landing page and each individual WP's landing page using Requests and BeautifulSoup            |
| [Federal Reserve Bank of Cleveland](https://www.clevelandfed.org/publications/working-paper)                                 | roundup_scripts/scrapers/Fed_Cleveland.py     | Reads main landing page using a headless instance of Chrome via Selenium, and parses using BeautifulSoup.   |
| [Federal Reserve Bank of Dallas](https://www.dallasfed.org/research/papers)                                 | roundup_scripts/scrapers/Fed_Dallas.py     | Scrapes main landing page using Requests and BeautifulSoup and also reads data from PDFs using PyPDF and io     |
| [Federal Reserve Bank of Kansas City](https://www.kansascityfed.org/research/research-working-papers/)                                 | roundup_scripts/scrapers/Fed_KansasCity.py     | Reads main landing page using Requests and parses with BeautifulSoup. Extracts data from each individual WP's landing page using Requests and BeautifulSoup    |
| [Federal Reserve Bank of Minneapolis](https://www.minneapolisfed.org/economic-research/working-papers)                                      | roundup_scripts/scrapers/Fed_Minneapolis.py         | Scrapes main landing page and each individual WP's landing page using Requests and BeautifulSoup           |
| [Federal Reserve Bank of New York](https://www.newyorkfed.org/research/staff_reports/index.html)                                 | roundup_scripts/scrapers/Fed_NewYork.py     | Uses Requests to access New York Fed API for JSON-formatted data on recent publications. Scrapes each individual WP's landing page using Requests and BeautifulSoup            |
| [Federal Reserve Bank of Philadelphia](https://www.philadelphiafed.org/search-results/all-work?searchtype=working-papers)                               | roundup_scripts/scrapers/Fed_Philadelphia.py     | Reads main landing page using Selenium and parses with BeautifulSoup. Extracts data from each individual WP's landing page using Requests and BeautifulSoup and reads PDF metadata using PyPDF2 and io       |
| [Federal Reserve Bank of Richmond](https://www.richmondfed.org/publications/research/working_papers)                               | roundup_scripts/scrapers/Fed_Richmond.py     | Reads main landing page using Selenium and parses with BeautifulSoup. Extracts data from each individual WP's landing page using Requests and BeautifulSoup and reads PDF metadata using PyPDF2 and io       |
| [Federal Reserve Bank of San Francisco](https://www.frbsf.org/economic-research/publications/working-papers/)                                | roundup_scripts/scrapers/Fed_SanFrancisco.py     | Uses Requests to acccess San Francisco Fed's API for JSON-formatted data on recent publications.   |
| [Federal Reserve Bank of St. Louis](https://research.stlouisfed.org/wp)                                | roundup_scripts/scrapers/Fed_StLouis.py     | Scrapes main landing page using Requests and BeautifulSoup.   |
| [International Monetary Fund](https://www.imf.org/en/Publications/RSS?language=eng&series=IMF%20Working%20Papers)                                      | roundup_scripts/scrapers/IMF.py         | Scrapes RSS feed using Feedparser. Scrapes each individual WP's landing page using Requests and BeautifulSoup            |
| [National Bureau of Economic Research](https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=100)                             | roundup_scripts/scrapers/NBER.py        | Interacts with NBER API and uses requests to parse the results  |


# Getting Started

The web scrapers are run remotely at 6:40 AM EST daily via the project GitHub Actions workflow located in `.github/workflows/main`. However, the web scrapers may also be operated on your local machine. See below for instructions on how to run the project for the first time on your local machine and any subsequent time.

### If running a local instance for the first time:

1. **Clone the repository:** 
  
    `git clone https://github.com/lorae/roundup`

2. **Set your working directory into the repository:**

   `cd ~/roundup`

3. **Create a [virtual environment](https://docs.python.org/3/library/venv.html):** 

   `python -m venv .venv`

4. **[Source](https://docs.python.org/3/library/venv.html#how-venvs-work) the virtual environment:**

    - **Using bash/zsh:**

        `source .venv/bin/activate`

    - **Using Windows PowerShell:**

         `.venv/Scripts/activate`

5. **Install dependencies**

    `python -m pip install -r requirements.txt`

6. **Start the script**

    `python runall.py`

7. **View results:**

    Local unique results will be stored in `historic/weekly_data/YYYY-MM-DD-HHMM.html`. "YYYY-MM-DD-HHMM" will be populated with the day, hour and minute that you ran the code.

    The interactive project dashboard on [https://roundup.streamlit.app](https://roundup.streamlit.app/) will not be updated unless you commit your changes to the main branch of the project. 

### If running a local instance again:
1. **Set your working directory into the repository:**

   `cd ~/roundup`

2. **[Source](https://docs.python.org/3/library/venv.html#how-venvs-work) the virtual environment:**

    - **Using bash/zsh:**

        `source .venv/bin/activate`

    - **Using Windows PowerShell:**

         `.venv/Scripts/activate`
3. **Start the script**

    `python runall.py`

4. **View results:**

    "New" results - those that have not yet appeared in `papers-we-have-seen.txt`, will be stored in `historic/weekly_data/YYYY-MM-DD-HHMM.html`. "YYYY-MM-DD-HHMM" will be populated with the day, hour and minute that you ran the code.

    The interactive project dashboard on [https://roundup.streamlit.app](https://roundup.streamlit.app/) will not be updated unless you commit your changes to the main branch of the project. 


# Project Structure
The schematic below illustrates the basic file structure of the project. 

roundup/
│
├── .gitignore
├── README.md
├── runall.py # Main project script
│
├── src/
│ ├── compare.py # Helper module for runall script
│ ├── streamlit_app.py # Script for producing Streamlit app
│ ├── scrapers_archive/ # Archival website-specific web scraping modules
│ └── scrapers/ # Website-specific web scraping modules
│   ├── BEA.py 
│   ├── BFI.py
│   ├── BIS.py
│   └── ...
│
├── data/
│ ├── papers-we-have-seen.txt/ # Set of unique IDs for data previously encountered
│ └── papers-we-have-seen-metadata.csv/ # Processed data goes here
│
├── .github/workflows/
│ └── main.yml # Runs `Daily Run` GitHub Actions workflow
│
└── requirements.txt # Project dependencies


**roundup**

The project directory.

- **runall.py**:  
  The main script in this project. It loops through each of the modules in `roundup_scripts/scrapers/XXX.py`, running their respective `XXX.scrape()` functions. This collects data from each website, which is then gathered into a large data frame.
  If an individual `XXX.scrape()` function produces an error, then the `runall.py` script will update that module's entry in `scraper_status.txt` to "off". If a `XXX.scrape()` function does not produce and error, then the `runall.py` script will update that module's entry in `scraper_status.txt` to "on". 
  
  After all web scrapers have been run and their data aggregated into a large data frame, `runall.py` invokes the `compare_historic(df)` function from the `roundup_scripts/compare.py` module to isolate only those data which are truly novel. `compare_historic(df)` uses data from `papers_we_have_seen.txt` as the source of historical truth in order to make this determination. Once `compare_historic(df)` has been successfully executed, new date- and time- stamped files are saved as `historic/weekly_data/YYYY-MM-DD-HHMM.csv`, `historic/weekly_data/YYYY-MM-DD-HHMM.txt`, and `historic/weekly_data/YYYY-MM-DD-HHMM.html` which contain metadata (title, authors, abstract, URL, date published, paper number, and unique paper ID number) on only the working papers that have not previously been scraped by runall.py. It will also append these new entries to `historic/papers-we-have-seen-metadata.csv`.

- **README.md**:  
  The document you are currently reading.

- **requirements.txt**:  
  A list of libraries and modules .

- **scraper_status.txt**:  
  A file that lists whether each scraper is operational ("on") or not ("off"). This file is used as input for the Streamlit app (`src/streamlit_app.py`), which displays scraper statuses in the side panel. A scraper status helps visitors of the website determine which web scrapers are currently operational. It also allows project developers to target modules for maintenance. The changing nature of websites means that even the most well-coded web scrapers will fail eventually.

- **historic**:  
  A folder containing data that has been previously scraped in this project.

    - **papers_we_have_seen.txt**:  
  A file that can be considered the main historical record of the project. It tells `compare.py` which papers we have seen and which we haven’t by storing all of the index numbers of the papers that have been seen as a python set. Note that no data is stored here aside from index numbers (this is a memory-saving feature of the repository).

    - **weekly_data**:  
  A folder containing the data that is gathered in every scrape of the project. Files are stored in the format `YYYY-MM-DD-HHMM.csv`, `YYYY-MM-DD-HHMM.txt`, and `YYYY-MM-DD-HHMM.html` for the time the code was run. The `.csv` and `.html` files contain the actual data that was newly seen in a given run of `runall.py`. This new data can easily be viewed using Microsoft Excel or using a browser. The `.txt` files are intended more for reference. They contain only the ID numbers of the of the novel data.

- **src**:  
  A folder containing all of the code used in the project, except for `runall.py`.
  - **compare.py**:  
    A module used within `runall.py`. Primary function of interest is `compare_historic(df)`, which takes the most recently scraped data as its only input argument and compares it to the data in `papers_we_have_seen.txt`. It then outputs the unique ID numbers and data corresponding with papers that are newly seen and saves the new data in the main database of the project, `historic/papers-we-have-seen-metadata.csv`, as well as local copies, `historic/weekly_data/YYYY-MM-DD-HHMM.csv` and `historic/weekly_data/YYYY-MM-DD-HHMM.txt`.

  - **scrapers**:  
    A folder that contains each of the individual web scraping modules. Each one is customized to a specific website such as BIS, Chicago Fed, NBER, etc. The scripts are named accordingly. All modules in this folder have analogous functions called `scrape()`, which aggregate data from their respective websites to output data frames. So, for example, in `runall.py`, we can import BIS and run `BIS.scrape()` to get the most recent data (formatted as a pandas data frame) from the Bank for International Settlements, or we can import NBER and run `NBER.scrape()` to get a data frame of the most recent data scraped from the National Bureau of Economic Research.
    
  - **scrapers_archive**:  
    A folder that contains potentially useful archived scraper code.
