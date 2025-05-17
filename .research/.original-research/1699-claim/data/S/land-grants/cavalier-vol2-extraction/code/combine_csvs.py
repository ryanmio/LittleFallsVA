#!/usr/bin/env python3
import pandas as pd
import os
import argparse

def combine_csv_files(input_dir, output_file):
    """
    Combine CSV files from books 9-14 into a single CSV file.
    
    Args:
        input_dir: Directory containing the individual book CSV files
        output_file: Path to save the combined CSV file
    """
    # List to store dataframes
    dfs = []
    
    # Process book 9-14 CSV files
    for book_num in range(9, 15):
        input_file = os.path.join(input_dir, f"book{book_num}_raw.csv")
        if os.path.exists(input_file):
            print(f"Processing {input_file}")
            df = pd.read_csv(input_file)
            dfs.append(df)
        else:
            print(f"Warning: {input_file} not found")
    
    if not dfs:
        print("No CSV files found to combine")
        return False
    
    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save combined dataframe to CSV
    combined_df.to_csv(output_file, index=False)
    print(f"Combined {len(dfs)} CSV files with a total of {len(combined_df)} entries")
    print(f"Output written to {output_file}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Combine book CSV files into a single CSV file")
    parser.add_argument("--input-dir", default="../extracted_entries", 
                        help="Directory containing the individual book CSV files")
    parser.add_argument("--output-file", default="../combined/books9-14.csv",
                        help="Path to save the combined CSV file")
    
    args = parser.parse_args()
    
    combine_csv_files(args.input_dir, args.output_file)

if __name__ == "__main__":
    main() 