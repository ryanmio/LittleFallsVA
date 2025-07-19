#!/usr/bin/env python3
"""
extract_book.py - Extract grant entries from OCR text files

Extracts individual land grant entries from a single OCR book file,
preserving the original text format. Creates a CSV with three columns:
- volume: always "II" for this project
- book: the book number
- raw_entry: the complete grant entry text as it appears in the source

Usage:
    python extract_book.py --input book9_ocr.txt --book 9 --output-dir ../extracted_entries
"""

import argparse
import csv
import os
import re
from pathlib import Path

def find_abstracts_start(text):
    """Find the starting position of the actual abstracts section."""
    # Look for the patent book header pattern
    pattern = re.compile(r'PATENT BOOK No\. \d+', re.IGNORECASE)
    match = pattern.search(text)
    if match:
        return match.start()
    return 0  # If not found, start from beginning

def clean_text(text):
    """Clean the text by removing headers and fixing hyphenation."""
    # Split into pages
    pages = text.split('\f')
    cleaned_pages = []
    
    # Regular expressions for headers and page numbers
    header_pattern = re.compile(r'^PATENT BOOK.*$', re.MULTILINE | re.IGNORECASE)
    page_num_pattern = re.compile(r'^\s*\d+\s*$', re.MULTILINE)
    
    for page in pages:
        lines = page.splitlines()
        
        # Skip empty pages
        if not lines:
            continue
            
        # Remove first two lines of each page (header and page number)
        if len(lines) >= 2:
            lines = lines[2:]
        
        # Filter out any remaining headers or lone page numbers
        filtered_lines = []
        for line in lines:
            if not header_pattern.match(line) and not page_num_pattern.match(line):
                filtered_lines.append(line)
        
        # Rejoin the lines
        cleaned_pages.append('\n'.join(filtered_lines))
    
    # Rejoin the pages with form-feeds
    cleaned_text = '\f'.join(cleaned_pages)
    
    # Fix hyphenation (replace hyphen + newline + optional whitespace with nothing)
    cleaned_text = re.sub(r'-\n\s*', '', cleaned_text)
    
    return cleaned_text

def extract_grants(text):
    """Extract complete land grant entries by identifying header patterns and continuing
    until the next header pattern is found.
    """
    # Split text into lines for processing
    lines = text.splitlines()
    
    entries = []
    current_entry = []
    in_entry = False
    
    # Find each start of an entry (defined as a line that follows a blank line,
    # is flush-left or nearly so, and starts with uppercase)
    i = 0
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        if not line_stripped:
            # Just skip blank lines
            i += 1
            continue
        
        # Calculate indent level (leading spaces)
        indent = len(line) - len(line.lstrip())
        
        # SUPER SIMPLE RULE: A header is ONLY a flush-left line after a blank line
        # and starts with at least 2 consecutive uppercase letters
        is_blank_before = (i == 0) or (not lines[i-1].strip())
        is_header = is_blank_before and indent <= 2 and re.match(r'[A-Z]{2,}', line_stripped)
        
        if is_header:
            # If we're already tracking an entry, save it before starting a new one
            if current_entry:
                entries.append('\n'.join(current_entry).strip())
            
            # Start a new entry
            current_entry = [line]
            in_entry = True
        elif in_entry:
            # Continue current entry
            current_entry.append(line)
        
        i += 1
    
    # Add the final entry if there is one
    if current_entry:
        entries.append('\n'.join(current_entry).strip())
    
    # Post-processing to validate and filter entries
    validated_entries = []
    for entry in entries:
        entry_text = entry.strip()
        
        # Minimal validation - entry should have a meaningful amount of text
        if len(entry_text) >= 50:
            # Skip boilerplate form templates that start with specific patterns
            first_line = entry_text.split('\n')[0].strip()
            skip_patterns = [
                "ANNE by the Grace of God",
                "GEORGE by the Grace of God",
                "WHEREAS by one Inquisition",
                "Form used for",
                "Form used in",
                "APPEARS that",
                "PROVIDED always"
            ]
            
            # Skip if first line matches any of the patterns
            if not any(pattern in first_line for pattern in skip_patterns):
                validated_entries.append(entry)
    
    return validated_entries

def main():
    parser = argparse.ArgumentParser(description='Extract grant entries from a book OCR file')
    parser.add_argument('--input', type=str, required=True, 
                        help='Input OCR text file (e.g., book9_ocr.txt)')
    parser.add_argument('--book', type=int, required=True,
                        help='Book number (e.g., 9)')
    parser.add_argument('--volume', type=str, default='II',
                        help='Volume number (default: II)')
    parser.add_argument('--output-dir', type=str, default='../extracted_entries',
                        help='Output directory for the CSV file')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Construct output file path
    output_file = output_dir / f"book{args.book}_raw.csv"
    
    # Read the input file
    with open(args.input, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Find and extract the abstracts section
    start_pos = find_abstracts_start(text)
    text = text[start_pos:]
    
    # Clean the text
    cleaned_text = clean_text(text)
    
    # Extract the grant entries
    entries = extract_grants(cleaned_text)
    
    # Write the entries to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['volume', 'book', 'raw_entry'])
        # Write entries
        for entry in entries:
            writer.writerow([args.volume, args.book, entry])
    
    print(f"Extracted {len(entries)} entries from book {args.book}")
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    main() 