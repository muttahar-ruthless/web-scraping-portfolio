import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

URL = "https://realpython.github.io/fake-jobs/"
OUTPUT_DIR = "output"

def scrape_jobs():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    job_cards = soup.select("div.card-content")

    jobs = []

    for job in job_cards:
        title = job.select_one("h2.title").text.strip()
        company = job.select_one("h3.company").text.strip()
        location = job.select_one("p.location").text.strip()
        link = job.select_one("a")["href"]

        jobs.append({
            "job_title": title,
            "company": company,
            "location": location,
            "job_url": link
        })

    return jobs

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Scraping job listings...")
    jobs = scrape_jobs()

    df = pd.DataFrame(jobs)

    csv_path = os.path.join(OUTPUT_DIR, "jobs.csv")
    excel_path = os.path.join(OUTPUT_DIR, "jobs.xlsx")

    from openpyxl.utils import get_column_letter

    df.to_csv(csv_path, index=False)

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Jobs")
        sheet = writer.sheets["Jobs"]

        # Freeze header row
        sheet.freeze_panes = "A2"

        # Enable filters
        sheet.auto_filter.ref = sheet.dimensions

        # Auto-adjust column widths
        for col_idx, col in enumerate(df.columns, start=1):
            max_length = max(
                df[col].astype(str).map(len).max(),
                len(col)
            )
            sheet.column_dimensions[get_column_letter(col_idx)].width = max_length + 3


        print(f"Saved CSV → {csv_path}")
        print(f"Saved Excel → {excel_path}")

if __name__ == "__main__":
    main()
