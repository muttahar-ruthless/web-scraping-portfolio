# PDF Invoice Data Extractor

A Python tool that extracts structured invoice data from PDF files
and converts them into clean CSV format.

## Extracted Fields
- Invoice number
- Invoice date
- Customer name
- VAT number
- Net total
- VAT amount
- Gross total

## Features
- Handles multi-page PDFs
- Robust regex-based field extraction
- Locale-aware number formatting
- Batch processing support

## How to Run
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python extractor.py
