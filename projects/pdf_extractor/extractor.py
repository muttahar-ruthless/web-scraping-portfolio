import pdfplumber
import pandas as pd
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def extract_full_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_field(pattern, text):
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else None

def clean_amount(value):
    if not value:
        return None
    value = value.replace(".", "").replace(",", ".")
    return float(value)

def extract_invoice_data(text):
    return {
        "invoice_number": extract_field(
            r"Invoice\s*No[\s\S]*?(\d{6,})",
            text
        ),
        "invoice_date": extract_field(
            r"Date[\s\S]*?([0-9]{1,2}\.\s*[A-Za-zäöüÄÖÜ]+\s*\d{4})",
            text
        ),
        "customer_name": extract_field(
            r"\n(Musterkunde AG)\n",
            text
        ),
        "vat_number": extract_field(
            r"VAT\s*No\.?\s*([A-Z0-9]+)",
            text
        ),
        "net_total": clean_amount(
            extract_field(r"Total\s+([0-9\.,]+)\s+€", text)
        ),
        "vat_amount": clean_amount(
            extract_field(r"VAT\s*19\s*%\s*([0-9\.,]+)\s+€", text)
        ),
        "gross_total": clean_amount(
            extract_field(
                r"Gross\s*Amount\s*incl\.?\s*VAT\s*([0-9\.,]+)\s+€",
                text
            )
        ),
    }

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for file in os.listdir(INPUT_DIR):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, file)
            print(f"Processing: {file}")

            text = extract_full_text(pdf_path)
            invoice_data = extract_invoice_data(text)

            df = pd.DataFrame([invoice_data])
            output_path = os.path.join(
                OUTPUT_DIR,
                file.replace(".pdf", "_invoice_summary.csv")
            )

            df.to_csv(output_path, index=False)
            print(f"Saved summary → {output_path}")

if __name__ == "__main__":
    main()
