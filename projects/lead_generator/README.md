# Business Lead Generator

A Python-based web scraping tool that collects lead-style data
from directory-style websites and exports it to CSV format.

## Data Extracted
- Name
- Profile URL

## Features
- Pagination handling
- Clean CSV output
- Duplicate removal
- Polite request delays

## Tools Used
- Python
- Requests
- BeautifulSoup
- Pandas

## How to Run
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python scraper.py
