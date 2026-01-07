from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os
import re

# ================= CONFIG =================
BASE_URL = "https://www.centris.ca/en/properties~for-sale"
MAX_PAGES = 2
WAIT_TIME = 15

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_city_from_url(url):
    try:
        # example:
        # /condos~for-sale~montreal-ville-marie/21093488
        part = url.split("~for-sale~")[1]
        city = part.split("/")[0]
        return city.replace("-", " ").title()
    except:
        return ""
def extract_price_from_nuxt(driver):
    try:
        html = driver.page_source

        # match price inside Nuxt state
        match = re.search(r'"price"\s*:\s*(\d{4,})', html)
        if match:
            price = match.group(1)
            return f"${int(price):,}"
        return ""
    except:
        return ""

def extract_price_from_json(driver):
    try:
        html = driver.page_source
        match = re.search(r'"price"\s*:\s*"?(\\$?[0-9,]+)"?', html)
        if match:
            return match.group(1)
        return ""
    except:
        return ""


# ================= HELPERS =================
def is_valid_listing(url):
    if not url:
        return False

    patterns = [
        "houses~for-sale",
        "condos~for-sale",
        "lots~for-sale",
        "duplexes~for-sale"
    ]

    if not any(p in url for p in patterns):
        return False

    return url.rstrip("/").split("/")[-1].isdigit()


def get_property_type(url):
    if "houses~for-sale" in url:
        return "House"
    if "condos~for-sale" in url:
        return "Condo"
    if "lots~for-sale" in url:
        return "Lot"
    if "duplexes~for-sale" in url:
        return "Duplex"
    return "Other"


# ================= DRIVER =================
options = Options()
options.page_load_strategy = "eager"

options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(30)
wait = WebDriverWait(driver, WAIT_TIME)

results = []

print("Opening Centris...")
driver.get(BASE_URL)
time.sleep(5)

# ================= SCRAPE =================
for page in range(1, MAX_PAGES + 1):
    print(f"\nScraping page {page}...")

    cards = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "a[href*='/en/']")
        )
    )

    raw_links = [c.get_attribute("href") for c in cards]
    listing_links = list(set([u for u in raw_links if is_valid_listing(u)]))

    print(f"Found {len(listing_links)} valid listings")

    for link in listing_links:
        try:
            driver.get(link)
            time.sleep(2)

            price = extract_price_from_nuxt(driver)
            city = extract_city_from_url(link)

            results.append({
                "price": price,
                "city": city,
                "property_type": get_property_type(link),
                "listing_url": link
            })

            print("✔", price, city)

        except Exception as e:
            print("✖ Skipped listing:", e)



    # NEXT PAGE
    try:
        next_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Next page']"))
        )
        next_btn.click()
        time.sleep(5)
    except:
        print("No next page. Stopping.")
        break

driver.quit()

# ================= SAVE =================
df = pd.DataFrame(results)
excel_path = os.path.join(OUTPUT_DIR, "centris_listings.xlsx")
df.to_excel(excel_path, index=False)

print(f"\nSaved → {excel_path}")
