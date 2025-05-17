#!/usr/bin/env python3

import os
import io
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

def extract_text_alternative(pdf_path):
    """Alternative method to extract text using PDFMiner components directly"""
    text = ""
    resource_manager = PDFResourceManager()
    fake_file_handle = StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=False):
            try:
                page_interpreter.process_page(page)
            except Exception as e:
                print(f"Error processing page: {e}")
                continue
            
        text = fake_file_handle.getvalue()
    
    # Close resources
    converter.close()
    fake_file_handle.close()
    
    return text

def extract_text_with_ocr(pdf_path, start_page=0, max_pages=None):
    """Extract text from PDF using OCR"""
    print("Using OCR to extract text from scanned PDF...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Convert PDF pages to images
        try:
            # Only process a subset of pages if needed (large PDFs can be memory-intensive)
            if max_pages is None:
                images = convert_from_path(pdf_path, dpi=300, first_page=start_page+1)
            else:
                images = convert_from_path(pdf_path, dpi=300, first_page=start_page+1, last_page=start_page+max_pages)
                
            print(f"Converted {len(images)} pages to images")
            
            # Extract text from each image using OCR
            text = ""
            for i, image in enumerate(images):
                if i % 5 == 0:  # Status update every 5 pages
                    print(f"Processing page {start_page + i + 1} with OCR...")
                page_text = pytesseract.image_to_string(image)
                text += f"\n\n=== Page {start_page + i + 1} ===\n\n"
                text += page_text
                
            return text
        except Exception as e:
            print(f"Error in OCR extraction: {e}")
            traceback.print_exc()
            return ""

def process_pdf(pdf_path, filename):
    print(f"Processing {filename}...")
    
    # First try the standard extraction method
    text = extract_text(pdf_path)
    
    # If we didn't get much text, try the alternative method
    if len(text.strip()) < 100:
        print(f"Standard extraction yielded little text, trying alternative method...")
        try:
            text = extract_text_alternative(pdf_path)
        except Exception as e:
            print(f"Error in alternative extraction: {e}")
            traceback.print_exc()
    
    # If still minimal text, try OCR (for books, process first 30 pages to start)
    if len(text.strip()) < 100:
        try:
            # For larger PDFs, we'll just process the first 30 pages to save time
            # Change max_pages=None to process all pages
            text = extract_text_with_ocr(pdf_path, start_page=0, max_pages=30)
        except Exception as e:
            print(f"Error in OCR extraction: {e}")
            traceback.print_exc()
    
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
    output_filename = os.path.splitext(filename)[0].replace(" ", "-").lower() + ".md"
    output_path = os.path.join(output_dir, output_filename)
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"Saved to {output_path}")
    print(f"Extracted text length: {len(text)} characters")

def main():
    pdf_dir = ".research/pdfs"
    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_dir, filename)
            process_pdf(pdf_path, filename)

if __name__ == "__main__":
    main() 