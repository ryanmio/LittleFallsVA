#!/usr/bin/env python3
"""
merge_books.py - Merge OCR output files for split books

This script concatenates OCR text files for books that were scanned in multiple parts,
preserving form-feed characters between pages.
"""

import argparse
from pathlib import Path

def merge_book_parts(output_dir, book_name, parts):
    """Merge multiple book parts into a single file with form-feeds between pages."""
    output_path = Path(output_dir) / f"{book_name}_ocr.txt"
    
    # Read all text content with form-feeds preserved
    all_text = ""
    
    for part in parts:
        part_path = Path(output_dir) / f"{part}_ocr.txt"
        if not part_path.exists():
            print(f"Warning: {part_path} not found!")
            continue
            
        print(f"Reading {part_path}")
        with open(part_path, 'r', encoding='utf-8') as f:
            text = f.read()
            if all_text and not all_text.endswith('\f\n'):
                all_text += '\f\n'  # Add form-feed between parts if needed
            all_text += text
    
    # Write merged content
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(all_text)
    
    print(f"Created merged file: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Merge OCR text files for books split into multiple parts')
    parser.add_argument('--output-dir', type=str, 
                        default="../OCR-output",
                        help='Directory containing OCR text files')
    args = parser.parse_args()
    
    # Define book parts to merge
    books_to_merge = {
        'book9': ['book9part1', 'book9part2'],
        'book10': ['book10', 'book10pt2'],
        'book11': ['book11'],  # Using the actual filename
        'book13': ['book13'],  # Using the actual filename
    }
    
    # Merge each book
    for book_name, parts in books_to_merge.items():
        merge_book_parts(args.output_dir, book_name, parts)
        
if __name__ == "__main__":
    main() 