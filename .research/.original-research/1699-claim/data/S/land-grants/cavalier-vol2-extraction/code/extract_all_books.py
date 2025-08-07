#!/usr/bin/env python3
"""
extract_all_books.py - Run the extraction process on all books

This script runs extract_book.py on each book in the OCR-output directory,
then creates a merged CSV with all entries.
"""

import argparse
import subprocess
import pandas as pd
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Extract grant entries from all books')
    parser.add_argument('--ocr-dir', type=str, default='../OCR-output',
                       help='Directory containing OCR text files')
    parser.add_argument('--output-dir', type=str, default='../extracted_entries',
                       help='Output directory for the CSV files')
    parser.add_argument('--merged-csv', type=str, default='../extracted_entries/volume_II_grants.csv',
                       help='Path to write the merged CSV file')
    
    args = parser.parse_args()
    
    ocr_dir = Path(args.ocr_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Define all books to process
    books = [9, 10, 11, 12, 13, 14]
    
    # Process each book
    for book in books:
        input_file = ocr_dir / f"book{book}_ocr.txt"
        if not input_file.exists():
            print(f"Warning: {input_file} not found, skipping book {book}")
            continue
        
        print(f"Processing book {book}...")
        cmd = [
            "python", "extract_book.py",
            "--input", str(input_file),
            "--book", str(book),
            "--output-dir", str(output_dir)
        ]
        subprocess.run(cmd, check=True)
    
    # Merge all CSVs into one
    all_dfs = []
    for book in books:
        csv_file = output_dir / f"book{book}_raw.csv"
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            all_dfs.append(df)
    
    if all_dfs:
        merged_df = pd.concat(all_dfs, ignore_index=True)
        merged_df.to_csv(args.merged_csv, index=False)
        print(f"Merged CSV with {len(merged_df)} entries written to {args.merged_csv}")
    else:
        print("No CSV files found to merge")

if __name__ == "__main__":
    main() 