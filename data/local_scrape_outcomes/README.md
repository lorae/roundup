# Local Scrape Outcomes

## Overview

This directory contains the output files from local data scraping operations, and provides a quick snapshot of what the web scraper has gathered (or if it worked at all). The contents of this directory - excluding this README that you are reading - are not tracked by version control (`.gitignore`), nor do they affect the database underlying this repository's Streamlit app. 

Because of this repository's automated GitHub Actions workflow, this directory remains unaffected when web scrapers are auto-run each day. Instead, files are only saved to this directory when you choose to run the script locally.

In prior iterations of this project, this functionality - particularly the HTML files - were produced weekly by manually running this repository's main script and presented as a weekly snapshot of economics research. Now that that process has been automated, this folder remains primarily for local usage and debugging.

## Contents

This directory may include the following files:
- **YYYY-MM-DD-HHMM-data.csv**: Contains all novel entries with metadata that were found when scraping was performed. Each file is timestamped based on when the scrape operation was completed.
- **YYYY-MM-DD-HHMM-dashboard.html**: Browser-viewable file that displays a dashboard of scraped data with clickable links for each entry. Contains all novel entries found when scraping was performed.
- **YYYY-MM-DD-HHMM-ids.txt**: Contains a set of unique identifiers for the novel entries found when scraping was performed.

## Configuration

Files in this directory are generated by the `HistoricDataComparer` class, which compares newly scraped data against a historical record to identify new entries. The class then saves these entries in various formats for local review using the `save_results()` method.

## Notes

- Please do not commit files in this directory to the repository; they are intentionally excluded via `.gitignore`.
- For more details on the operation and configuration of the data scraping and comparison, refer to the main project `README.md` or the source code documentation in the `src` directory.
