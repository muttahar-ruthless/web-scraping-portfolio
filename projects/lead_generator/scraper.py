import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

BASE_URL = "https://quotes.toscrape.com/page/{}/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (LeadGeneratorBot/1.0)"
}

OUTPUT_DIR = "output"

def scrape_page(page):
    url = BASE_URL.format(page)
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    quotes = soup.select(".quote")

    leads = []

    for q in quotes:
        author = q.select_one(".author").text.strip()
        author_link = q.select_one("a")["href"]
        profile_url = "https://quotes.toscrape.com" + author_link

        leads.append({
            "name": author,
            "profile_url": profile_url
        })

    return leads

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_leads = []

    for page in range(1, 6):
        print(f"Scraping page {page}")
        try:
            page_leads = scrape_page(page)
            all_leads.extend(page_leads)
            time.sleep(1)
        except Exception as e:
            print(f"Error on page {page}: {e}")

    df = pd.DataFrame(all_leads).drop_duplicates()
    output_path = os.path.join(OUTPUT_DIR, "leads.csv")
    df.to_csv(output_path, index=False)

    print(f"Saved leads → {output_path}")

if __name__ == "__main__":
    main()
