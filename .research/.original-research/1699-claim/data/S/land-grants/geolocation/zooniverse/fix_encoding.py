#!/usr/bin/env python3
"""
fix_encoding.py

Fixes encoding issues in the Zooniverse manifest files, particularly:
- "Äôs" → "'s" (apostrophe issue)
- Other common encoding problems

Usage:
    python3 fix_encoding.py --input manifest.csv --output manifest_fixed.csv
    python3 fix_encoding.py --input manifest_caption.csv --output manifest_caption_fixed.csv
"""

import argparse
import csv
import pathlib
import re

def fix_encoding(text):
    """Fix common encoding problems in text."""
    if not isinstance(text, str):
        return text
        
    # Fix apostrophes
    text = text.replace("Äôs", "'s")
    text = text.replace("‚Äôs", "'s")
    text = text.replace("‚'s", "'s") # Already partially fixed
    
    # Fix other common problems
    text = text.replace("‚Äò", "'")    # Opening single quote
    text = text.replace("‚Äù", '"')    # Closing double quote
    text = text.replace("‚Äú", '"')    # Opening double quote
    text = text.replace("‚Äô", "'")    # Closing single quote
    text = text.replace("‚'", "'")     # Already partially fixed
    text = text.replace("\u00A0", " ") # Non-breaking space
    text = text.replace("¬ß", "S")     # Broken S character
    
    # For the specific pattern in the sample data
    text = text.replace("‚Ä", "'")     # Aggressive replacement for common error prefix
    text = text.replace("‚", "'")      # Other broken apostrophe
    
    return text

def process_file(input_path, output_path):
    """Read input CSV, fix encoding issues, and write to output CSV."""
    rows = []
    
    with open(input_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        
        for row in reader:
            fixed_row = {k: fix_encoding(v) for k, v in row.items()}
            rows.append(fixed_row)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Processed {len(rows)} rows from {input_path} → {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Fix encoding issues in Zooniverse manifest files")
    parser.add_argument("--input", type=pathlib.Path, required=True, help="Input CSV file")
    parser.add_argument("--output", type=pathlib.Path, required=True, help="Output CSV file")
    args = parser.parse_args()
    
    process_file(args.input, args.output)

if __name__ == "__main__":
    main() 