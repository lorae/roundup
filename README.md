# About

The purpose of this project is to scrape various websites where economics working papers – papers that haven’t been peer reviewed yet – are published, so that the newest research can be tracked and aggregated. The basic project runs several Python scripts that each scrape a specific website and extract data: The title of the paper, its author(s), the date it was posted, a link to the text, an ID number (using the numbering system of the publishing website), and an abstract. Data from all sources are then combined and compared to previous scrapes. Those papers that haven’t been seen before – the newest papers – are outputted to an html file.

Websites that are scraped for data, as of August 2023, are:

| Name of website                                                  | Name of script                          | Scraping method |
|------------------------------------------------------------------|-----------------------------------------|-----------------|
| [Bureau of Economic Analysis](https://www.bea.gov/research/papers)                                      | roundup_scripts/scrapers/BEA.py         | Scrapes main landing page and each individual WP's landing page using Requests and BeautifulSoup           |
| [Becker Friedman Institute](https://www.bea.gov/research/papers) (at the University of Chicago)       | roundup_scripts/scrapers/BFI.py         | Scrapes main landing page and each individual WP's landing page using Requests and BeautifulSoup         |
| [Bank for International Settlements](https://www.bis.org/doclist/wppubls.rss?from=&till=&objid=wppubls&page=&paging_length=10&sort_list=date_desc&theme=wppubls&ml=false&mlurl=&emptylisttext=)                                | roundup_scripts/scrapers/BIS.py         | Scrapes RSS feed using Feedparser     |
| [Bank of England](https://www.bankofengland.co.uk/rss/publications)                                                  | roundup_scripts/scrapers/BOE.py         | Scrapes RSS feed using Feedparser and each individual WP's landing page using Requests and BeautifulSoup           |
| [European Central Bank](https://www.ecb.europa.eu/rss/wppub.html)                                            | roundup_scripts/scrapers/ECB.py         | Scrapes RSS feed using Feedparser and each individual WP's PDF using PyPDF2 and io          |
| [Federal Reserve Bank of Atlanta](https://www.atlantafed.org/rss/wps)                                 | roundup_scripts/scrapers/Fed_Atlanta.py     | Scrapes RSS feed using Feedparser             |
| [Federal Reserve Board of Governors](https://www.federalreserve.gov/econres/feds/index.htm) (of the United States): working papers | roundup_scripts/scrapers/Fed_Board.py       | Scrapes main landing page using Requests and BeautifulSoup             |
| [Federal Reserve Board of Governors](https://www.federalreserve.gov/econres/notes/feds-notes/default.htm) (of the United States): Fed Notes | roundup_scripts/scrapers/Fed_Board_Notes.py       | Scrapes main landing page using Requests and BeautifulSoup             |
| [Federal Reserve Bank of Boston](https://www.bostonfed.org/publications/research-department-working-paper/)                               | roundup_scripts/scrapers/Fed_Boston.py     | RSS             |
| [Federal Reserve Bank of Chicago](https://www.chicagofed.org/publications/publication-listing?filter_series=18)                                | roundup_scripts/scrapers/Fed_Chicago.py     | RSS             |
| [Federal Reserve Bank of Cleveland](https://www.clevelandfed.org/publications/working-paper)                                 | roundup_scripts/scrapers/Fed_Cleveland.py     | RSS             |
| [Federal Reserve Bank of Dallas](https://www.dallasfed.org/research/papers)                                 | roundup_scripts/scrapers/Fed_Dallas.py     | RSS             |
| [Federal Reserve Bank of New York](https://www.newyorkfed.org/research/staff_reports/index.html)                                 | roundup_scripts/scrapers/Fed_NewYork.py     | RSS             |
| [Federal Reserve Bank of San Francisco](https://www.frbsf.org/economic-research/publications/working-papers/)                                | roundup_scripts/scrapers/Fed_SanFrancisco.py     | RSS             |
| [International Monetary Fund](https://www.imf.org/en/Publications/RSS?language=eng&series=IMF%20Working%20Papers)                                      | roundup_scripts/scrapers/IMF.py         | RSS             |
| [National Bureau of Economic Research](https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=100)                             | roundup_scripts/scrapers/NBER.py        | RSS             |



# Getting started

### Clone and `cd` into the repository:

`git clone https://github.com/lorae/roundup`
`cd ~/roundup`

### Create a [virtual environment](https://docs.python.org/3/library/venv.html)

`python -m venv .venv`

### [Source](https://docs.python.org/3/library/venv.html#how-venvs-work) the virtual environment

**bash/zsh**

`source .venv/bin/activate`

**Windows powershell**

`.venv/Scripts/Activate.ps1`

### Install dependencies

`python -m pip install -r requirements.txt`

### Start the script

`python runall.py`




