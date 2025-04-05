#!/usr/bin/env python3

import os
import io
import sys
import re
import traceback
from pdfminer.high_level import extract_text
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from datetime import datetime
import pytesseract
from pdf2image import convert_from_path
import tempfile
import argparse

# Create output directory if it doesn't exist
output_dir = ".research/pdf_extracts"
os.makedirs(output_dir, exist_ok=True)

# Front matter data 
front_matter = {
    "Falls Church City Schools A History (1999).pdf": {
        "title": "Falls Church City Schools: A History",
        "creator": "Falls Church City Public Schools",
        "date": "1999",
        "format": "Books",
        "subject": "Falls Church City Public Schools",
        "identifier": "Falls Church City Schools A History (1999)",
        "source": "https://archive.mrspl.org/Documents/Detail/falls-church-city-schools-a-history/39063",
        "topics": "Falls Church history, education, schools, public schools, history"
    },
    "Falls Church _Virginia Village Revisited.pdf": {
        "title": "Falls Church: A Virginia Village Revisited",
        "creator": "Unknown", # Can be updated if known
        "date": "Unknown", # Can be updated if known
        "format": "Books",
        "subject": "Falls Church, Virginia",
        "identifier": "Falls Church _Virginia Village Revisited",
        "source": "https://archive.mrspl.org/Documents/Detail/falls-church-a-virginia-village-revisited/38847",
        "topics": "Falls Church history, Virginia, local history"
    }
}

def extract_text_with_ocr(pdf_path, start_page=0, max_pages=None, batch_size=10):
    """Extract text from PDF using OCR, processing in batches to avoid memory issues"""
    print("Using OCR to extract text from scanned PDF...")
    
    all_text = ""
    current_page = start_page
    
    try:
        # Get total number of pages
        import subprocess
        result = subprocess.run(['pdfinfo', pdf_path], capture_output=True, text=True)
        pages_line = [line for line in result.stdout.split('\n') if 'Pages:' in line]
        if pages_line:
            total_pages = int(pages_line[0].split('Pages:')[1].strip())
            print(f"PDF has {total_pages} total pages")
        else:
            print("Couldn't determine total page count, will process until the end")
            total_pages = float('inf') if max_pages is None else (start_page + max_pages)
    except Exception as e:
        print(f"Error getting page count: {e}")
        total_pages = float('inf') if max_pages is None else (start_page + max_pages)
    
    while current_page < total_pages:
        if max_pages is not None and current_page >= start_page + max_pages:
            break
            
        end_page = min(current_page + batch_size, total_pages)
        print(f"Processing batch: pages {current_page+1} to {end_page}")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Convert PDF pages to images for this batch
                images = convert_from_path(
                    pdf_path, 
                    dpi=300, 
                    first_page=current_page+1, 
                    last_page=end_page
                )
                
                print(f"Converted {len(images)} pages to images")
                
                # Extract text from each image using OCR
                for i, image in enumerate(images):
                    page_num = current_page + i + 1
                    print(f"Processing page {page_num} with OCR...")
                    
                    page_text = pytesseract.image_to_string(image)
                    all_text += f"\n\n=== Page {page_num} ===\n\n"
                    all_text += page_text
                    
                # Move to next batch
                current_page = end_page
                
            except Exception as e:
                print(f"Error in OCR extraction batch: {e}")
                traceback.print_exc()
                # Try to continue with next batch
                current_page = end_page
    
    return all_text

def process_pdf(pdf_path, filename, args):
    print(f"Processing {filename}...")
    
    # For scanned PDFs that need OCR
    if args.ocr:
        print("Using OCR method directly as specified...")
        text = extract_text_with_ocr(pdf_path, start_page=args.start_page, max_pages=args.max_pages)
    else:
        # First try the standard extraction method
        text = extract_text(pdf_path)
        
        # If we didn't get much text, try OCR
        if len(text.strip()) < 100:
            print(f"Standard extraction yielded little text, trying OCR...")
            text = extract_text_with_ocr(pdf_path, start_page=args.start_page, max_pages=args.max_pages)
    
    # Get frontmatter for this file
    metadata = front_matter.get(filename, {})
    if not metadata:
        print(f"Warning: No front matter found for {filename}")
        return
    
    # Create frontmatter in markdown format
    front_matter_md = "---\n"
    for key, value in metadata.items():
        front_matter_md += f"{key}: \"{value}\"\n"
    front_matter_md += f"type: \"book extract\"\n"
    front_matter_md += f"extract_date: \"{datetime.now().strftime('%Y-%m-%d')}\"\n"
    front_matter_md += "---\n\n"
    
    # Combine frontmatter and text
    full_content = front_matter_md + text
    
    # Create sanitized filename for output
    output_base = os.path.splitext(filename)[0].replace(" ", "-").lower()
    
    # Add suffix for partial extracts
    if args.max_pages is not None:
        end_page = args.start_page + args.max_pages
        output_filename = f"{output_base}-pages-{args.start_page+1}-to-{end_page}.md"
    else:
        output_filename = f"{output_base}-full.md"
        
    output_path = os.path.join(output_dir, output_filename)
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"Saved to {output_path}")
    print(f"Extracted text length: {len(text)} characters")

def main():
    parser = argparse.ArgumentParser(description='Extract text from PDF files with OCR')
    parser.add_argument('--pdf', help='Specific PDF file to process')
    parser.add_argument('--ocr', action='store_true', help='Force OCR processing')
    parser.add_argument('--start-page', type=int, default=0, help='Starting page (0-indexed)')
    parser.add_argument('--max-pages', type=int, help='Maximum number of pages to process')
    args = parser.parse_args()
    
    pdf_dir = ".research/pdfs"
    
    if args.pdf:
        # Process a single PDF
        pdf_path = args.pdf if os.path.isabs(args.pdf) else os.path.join(pdf_dir, args.pdf)
        if not os.path.exists(pdf_path):
            print(f"Error: File {pdf_path} not found")
            return
        filename = os.path.basename(pdf_path)
        process_pdf(pdf_path, filename, args)
    else:
        # Process all PDFs in the directory
        for filename in os.listdir(pdf_dir):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(pdf_dir, filename)
                process_pdf(pdf_path, filename, args)

if __name__ == "__main__":
    main() 