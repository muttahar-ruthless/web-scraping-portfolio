import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def scrape_page(page_number):
    url = BASE_URL.format(page_number)
    print(f"Requesting: {url}")

    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    books = soup.select("article.product_pod")

    print(f"Found {len(books)} books on page {page_number}")

    data = []

    for book in books:
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text.replace("£", "")
        availability = book.select_one(".availability").text.strip()
        rating = book.p["class"][1]

        data.append({
            "title": title,
            "price_gbp": price,
            "availability": availability,
            "rating": rating
        })

    return data

def main():
    print("Scraper started")

    all_books = []

    for page in range(1, 6):
        try:
            page_data = scrape_page(page)
            all_books.extend(page_data)
            time.sleep(1)
        except Exception as e:
            print(f"Error on page {page}: {e}")

    print(f"Total books scraped: {len(all_books)}")

    if not all_books:
        print("No data scraped. CSV will not be created.")
        return

    os.makedirs("output", exist_ok=True)

    df = pd.DataFrame(all_books)
    df.to_csv("output/books.csv", index=False)

    print("CSV saved successfully → output/books.csv")

if __name__ == "__main__":
    main()
