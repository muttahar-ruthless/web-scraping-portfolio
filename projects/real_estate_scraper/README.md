# Real Estate Listings Scraper

Scrapes real estate property listings from Centris.ca and exports
the data into Excel format using Selenium.

## Data Extracted
- City / Area
- Property type (House, Condo, Lot, Duplex)
- Listing URL

> Note: Price data on Centris is loaded via region-restricted APIs.
> Without Canadian IP access, prices may not be visible.  
> The scraper reliably extracts all non-restricted listing metadata.

## Output
- centris_listings.xlsx (clean Excel file, ready for analysis)

## How to Run
```bash
python scraper.py
